import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show the home page with current balance, last income, and transaction history"""
    user_id = session["user_id"]

    # Calculate user balance
    total_income = db.execute("SELECT SUM(amount) AS total FROM transactions WHERE user_id = ? AND type = 'income'", user_id)[0]["total"] or 0
    total_expenses = db.execute("SELECT SUM(amount) AS total FROM transactions WHERE user_id = ? AND type = 'expense'", user_id)[0]["total"] or 0
    user_balance = total_income - total_expenses

    # Fetch the last income entry
    last_income = db.execute("SELECT * FROM transactions WHERE user_id = ? AND type = 'income' ORDER BY time DESC LIMIT 1", user_id)
    last_income_entry = last_income[0] if last_income else None  # Get the last entry or None if there are no entries

    # Fetch all transactions for history
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY time DESC", user_id)

    return render_template("index.html", user_balance=user_balance, last_income_entry=last_income_entry, transactions=transactions)

@app.route("/add_expense", methods=["GET", "POST"])
@login_required
def add_expense():
    """Add an expense"""
    if request.method == "POST":
        description = request.form.get("description")
        amount = request.form.get("amount")
        category = request.form.get("category")

        if not description:
            return apology("Must provide a description", 400)
        elif not amount or not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
            return apology("Must provide a positive number", 400)

        user_id = session["user_id"]
        db.execute("INSERT INTO transactions (user_id, description, amount, type, category) VALUES (?, ?, ?, 'expense', ?)",
                   user_id, description, float(amount), category)

        flash("Expense added successfully!")
        return redirect("/")

    else:
        return render_template("add_expense.html")

@app.route("/add_income", methods=["GET", "POST"])
@login_required
def add_income():
    """Add an income"""
    if request.method == "POST":
        description = request.form.get("description")
        amount = request.form.get("amount")
        category = request.form.get("category")

        if not description:
            return apology("Must provide a description", 400)
        elif not amount or not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
            return apology("Must provide a positive number", 400)

        user_id = session["user_id"]
        db.execute("INSERT INTO transactions (user_id, description, amount, type, category) VALUES (?, ?, ?, 'income', ?)",
                   user_id, description, float(amount), category)

        flash("Income added successfully!")
        return redirect("/")

    else:
        return render_template("add_income.html")

@app.route("/view_history", methods=["GET"])
@login_required
def view_history():
    """View all income and expenses"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY time DESC", user_id)
    return render_template("view_history.html", transactions=transactions)

@app.route("/delete_transaction", methods=["POST"])
@login_required
def delete_transaction():
    """Delete a transaction"""
    transaction_id = request.form.get("transaction_id")
    user_id = session["user_id"]

    # Delete the transaction based on the transaction_id and user_id
    db.execute("DELETE FROM transactions WHERE id = ? AND user_id = ?", transaction_id, user_id)
    flash("Transaction deleted successfully!")
    return redirect("/view_history")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Must provide username", 400)
        elif not password:
            return apology("Must provide password", 400)
        elif password != confirmation:
            return apology("Passwords must match", 400)

        hash = generate_password_hash(password)

        try:
            new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("Username already taken", 400)

        session["user_id"] = new_user_id
        return redirect("/")

    else:
        return render_template("register.html")

# Ensure to create tables for expenses and income
if __name__ == "__main__":
    db.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, description TEXT NOT NULL, amount REAL NOT NULL, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id))")
    db.execute("CREATE TABLE IF NOT EXISTS income (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, description TEXT NOT NULL, amount REAL NOT NULL, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id))")
    app.run()
