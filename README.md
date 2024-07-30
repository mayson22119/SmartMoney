# SmartMoney
#### Video Demo: https://youtu.be/JWLcTH-_SxY
#### Description:
# Web application for managing personal finances
Welcome to the web application for managing your personal finances! Users who use this service can handle their own finances. Maintaining your financial well-being is more crucial than ever. Users of this web program can categorize transactions, keep tabs on their earnings and outlays, and access their financial history.

### Features

- User authentication: This program offers a safe means of authenticating users and preserving database information. Every user has a password that is stored in the finance.db database and is hashed.

- Income and cost management: By simply clicking the buttons below, you can add your income or expenses.

- Connection History: By selecting View History, users can view a history of their earnings or outlays.

- Record Deletion: Users are able to remove expenses and income.

### Installation
To get started with the application, follow these installation steps:

1. Download the Source Code. And exctract it.

2. Install Required Packages: You need to ensure that you have Python and pip installed on your machine. Navigate to the project directory in your terminal and run the following command to install all requirements packages:
"pip install -r requirements.txt"

### Running the Application

1. Open your terminal or command prompt.
2. Change to the directory where the project is located.
3. Start the Flask server by executing: "flask run"
4. By default, the application will run on http://127.0.0.1:5000/. Open this URL in your web browser to access the application.

### Usage

- Register for a New Account: To started, user must create their own account. It needs only a username and password, that typed two times.

- Log In: After registration, you can login into your created account. That will give you access to all the features of the application.

- Add Income and Expenses: You can record transactions by entering details (as the amount, category, and date). This feature allows to categorize transactions effectively, making it easier to analyze spending categories.

- View Transactions and Balance: You can view your transactions on homepage and also on history.

### Design Choices
User Authentication: For user authentication, Flask's session management was chosen due to its simplicity and effectiveness in handling logins and session data securely.

Data Storage
SQLite3 was selected for its lightweight nature and ease of use. It is an excellent choice for this application, providing a straightforward way to manage user data and transactions without the overhead of a more complex database system.

Frontend Design
The design of SmartMoney is kept simple and intuitive, with a few buttons at the top for easy navigation. Clicking on "SmartMoney" redirects users to the homepage, while "Add Income," "Add Expense," and "View History" buttons lead to the respective pages. Bootstrap is used to ensure the site is visually appealing and responsive across various device

### How it works
#### File structure
- SmartMoney/
- │
- ├── app.py                  # Main application file
- ├── finance.db              # SQLite database file
- ├── requirements.txt        # Python packages required for the project
- ├── static/                 # Static files
- │   └── logo.png            # Logo image
- ├── templates/              # HTML templates
- │   ├── layout.html         # Base layout template
- │   ├── apology.html        # Apology template
- │   ├── index.html          # Homepage template
- │   ├── login.html          # Login page template
- │   ├── register.html       # Registration page template
- │   ├── add_income.html     # Add income page template
- │   ├── add_expense.html    # Add expense page template
- │   └── view_history.html   # Transaction history page template
- └── README.md               # Project documentation

#### Flask
Flask is using app.py to create a dynamic webapp using templates folder.

#### SQLite
There is a database "finance.db" that contains table: users and transactions for using in webapp for storing users and all the transactions.

## Contributing
If you have suggestions for new features, improvements, or any other feedback, please feel free to submit a pull request. Collaboration is key to improving this application and making it more helpful and functionaly.
# SmartMoney
