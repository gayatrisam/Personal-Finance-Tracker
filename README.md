# Personal Finance Tracker

This is a Personal Finance Tracker application built using Python, Tkinter, SQLite, and Matplotlib. It allows users to track their income and expenses, visualize spending, and export financial reports.

## Features
- Add and delete transactions (Income/Expense)
- View transaction history in a table
- Set a budget limit and receive alerts when exceeded
- Visualize expenses by category using a pie chart
- Compare income vs. expenses using a bar chart
- Export financial data to CSV or Excel

## Technologies Used
- Python
- Tkinter (for GUI)
- SQLite (for database management)
- Matplotlib (for data visualization)
- Pandas (for exporting data to CSV/Excel)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/finance-tracker.git
   cd finance-tracker
   ```
2. Install dependencies:
   ```sh
   pip install matplotlib pandas openpyxl
   ```
3. Run the application:
   ```sh
   python finance_tracker.py
   ```

## Usage
1. Enter transaction details (Type, Category, Amount, Date)
2. Click "Add Transaction" to save it to the database
3. Use "Visualize Expenses" and "Visualize Income vs Expenses" for graphical insights
4. Export data using "Export CSV" or "Export Excel"
5. Set a budget limit to get notified when expenses exceed the limit


## Project Structure
```
finance-tracker/
│── finance_tracker.py   # Main Python script
│── finance_tracker.db   # SQLite database (created automatically)
│── requirements.txt     # Dependencies
│── README.md            # Project documentation
│── screenshot.png       # Screenshot of the application
```

## How to Push to GitHub
1. Initialize Git repository (if not done already):
   ```sh
   git init
   ```
2. Add files to staging area:
   ```sh
   git add .
   ```
3. Commit changes:
   ```sh
   git commit -m "Initial commit"
   ```
4. Create a new repository on GitHub and copy the remote URL.
5. Add the remote repository:
   ```sh
   git remote add origin https://github.com/your-username/finance-tracker.git
   ```
6. Push the code to GitHub:
   ```sh
   git branch -M main
   git push -u origin main
   ```

## License
This project is licensed under the MIT License.

## Contributing
Feel free to fork the repository and submit pull requests.

---

### Notes:
- Ensure Python is installed on your system.
- Replace `your-username` with your actual GitHub username in the repository URL.

---

### Notes:
- Ensure Python is installed on your system.
- Replace `your-username` with your actual GitHub username in the repository URL.
