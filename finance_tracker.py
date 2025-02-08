import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import pandas as pd

# Database setup
def setup_db():
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Function to add a transaction
def add_transaction():
    t_type = type_var.get()
    category = category_var.get()
    amount = amount_entry.get()
    date = date_entry.get()

    if not category or not amount or not date:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")
        return

    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, ?)",
                   (t_type, category, amount, date))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Transaction added successfully!")
    clear_entries()
    update_table()
    check_budget_limit()

# Function to update table with transaction history
def update_table():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", "end", values=row)

# Function to visualize expenses
def visualize_expenses():
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM transactions WHERE type='Expense' GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    if data:
        categories, amounts = zip(*data)
        plt.figure(figsize=(6, 4))
        plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
        plt.title("Expense Distribution")
        plt.show()
    else:
        messagebox.showinfo("Info", "No expense data available to visualize.")

# Function to visualize income vs expenses
def visualize_income_vs_expenses():
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type")
    data = cursor.fetchall()
    conn.close()

    if data:
        categories, amounts = zip(*data)
        plt.figure(figsize=(6, 4))
        plt.bar(categories, amounts, color=['green', 'red'])
        plt.title("Income vs Expenses")
        plt.xlabel("Transaction Type")
        plt.ylabel("Amount")
        plt.show()
    else:
        messagebox.showinfo("Info", "No data available to visualize.")

# Function to export data to CSV or Excel
def export_data(file_type):
    conn = sqlite3.connect("finance_tracker.db")
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()

    if file_type == "csv":
        df.to_csv("financial_report.csv", index=False)
        messagebox.showinfo("Success", "Financial report exported to CSV successfully!")
    elif file_type == "excel":
        df.to_excel("financial_report.xlsx", index=False, engine="openpyxl")
        messagebox.showinfo("Success", "Financial report exported to Excel successfully!")

# Function to set a spending limit and check against it
def check_budget_limit():
    try:
        limit = float(limit_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid budget limit!")
        return

    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
    total_expense = cursor.fetchone()[0] or 0
    conn.close()

    if total_expense > limit:
        messagebox.showwarning("Warning", f"Spending limit exceeded! Total Expenses: {total_expense}")

# Function to delete a selected transaction
def delete_transaction():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "No transaction selected!")
        return

    transaction_id = tree.item(selected_item)["values"][0]

    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Transaction deleted successfully!")
    update_table()

# Function to clear input fields
def clear_entries():
    category_var.set("")
    amount_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("750x600")

# Input fields
tk.Label(root, text="Transaction Type:").grid(row=0, column=0, padx=5, pady=5)
type_var = tk.StringVar(value="Expense")
ttk.Combobox(root, textvariable=type_var, values=["Income", "Expense"]).grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Category:").grid(row=1, column=0, padx=5, pady=5)
category_var = tk.StringVar()
ttk.Combobox(root, textvariable=category_var, values=["Food", "Rent", "Bills", "Entertainment", "Savings", "Other"]).grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Amount:").grid(row=2, column=0, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(root, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(root, text="Budget Limit:").grid(row=4, column=0, padx=5, pady=5)
limit_entry = tk.Entry(root)
limit_entry.grid(row=4, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text="Add Transaction", command=add_transaction).grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(root, text="Delete Transaction", command=delete_transaction).grid(row=6, column=0, columnspan=2, pady=5)
tk.Button(root, text="Visualize Expenses", command=visualize_expenses).grid(row=7, column=0, pady=5)
tk.Button(root, text="Visualize Income vs Expenses", command=visualize_income_vs_expenses).grid(row=7, column=1, pady=5)
tk.Button(root, text="Export CSV", command=lambda: export_data("csv")).grid(row=8, column=0, pady=5)
tk.Button(root, text="Export Excel", command=lambda: export_data("excel")).grid(row=8, column=1, pady=5)

# Transaction History Table
tree = ttk.Treeview(root, columns=("ID", "Type", "Category", "Amount", "Date"), show="headings")
tree.grid(row=9, column=0, columnspan=2, pady=10)
tree.heading("ID", text="ID")
tree.heading("Type", text="Type")
tree.heading("Category", text="Category")
tree.heading("Amount", text="Amount")
tree.heading("Date", text="Date")

update_table()
setup_db()
root.mainloop()
