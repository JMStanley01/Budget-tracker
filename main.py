import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime


def add_expense(expenses, description, amount, category):
    date = datetime.now().strftime("%Y-%m-%d")  # Automatically add the current date
    expenses.append({"description": description, "amount": amount, "category": category, "date": date})
    print(f"Added expense: {description}, Amount: {amount}, Category: {category}, Date: {date}")


def update_expense(expenses, description, new_description, new_amount):
    for expense in expenses:
        if expense['description'] == description:
            expense['description'] = new_description
            expense['amount'] = new_amount
            print(f"Updated expense: {description} -> {new_description}, Amount: {new_amount}")
            return True
    return False


def remove_expense(expenses, description):
    for expense in expenses:
        if expense['description'] == description:
            expenses.remove(expense)
            print(f"Removed expense: {description}")
            return True
    return False


def get_total_expenses(expenses):
    return sum(expense['amount'] for expense in expenses)


def get_balance(budget, expenses):
    return budget - get_total_expenses(expenses)


def load_budget_data(filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            return data.get('initial_budget', 0), data.get('expenses', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return 0, []  # Return default values if the file doesn't exist or is empty/corrupted


def save_budget_data(filepath, initial_budget, expenses):
    try:
        data = {
            'initial_budget': initial_budget,
            'expenses': expenses
        }
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print("Budget data saved successfully.")
    except Exception as e:
        print(f"An error occurred while saving data: {e}")


def update_expenses_gui(expense_listbox, expenses, budget):
    """Update the Listbox with the latest expenses."""
    expense_listbox.delete(0, tk.END)  # Clear the Listbox
    total_spent = get_total_expenses(expenses)
    for expense in expenses:
        percentage = (expense['amount'] / total_spent) * 100 if total_spent > 0 else 0
        expense_listbox.insert(
            tk.END,
            f"{expense['date']} - {expense['description']} ({expense['category']}): ${expense['amount']:.2f} ({percentage:.2f}%)"
        )
    expense_listbox.insert(tk.END, f"Total Spent: ${total_spent:.2f}")
    expense_listbox.insert(tk.END, f"Remaining Budget: ${get_balance(budget, expenses):.2f}")




def main():
    # Load data
    filepath = 'budget_data.json'
    initial_budget, expenses = load_budget_data(filepath)

    if initial_budget == 0:  # If no budget is found, prompt the user to set one
        initial_budget = float(input("Please enter your initial budget: "))
    budget = initial_budget  # Set the budget to the loaded or newly entered value

    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Budget Tracker")

    # Create a frame for the expenses
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Add a label
    ttk.Label(frame, text="Current Expenses", font=("Arial", 14)).grid(row=0, column=0, sticky=tk.W)

    # Create a Listbox to display expenses
    expense_listbox = tk.Listbox(frame, width=80, height=20)
    expense_listbox.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E))

    # Populate the Listbox with expenses
    update_expenses_gui(expense_listbox, expenses, budget)

    # Add input fields and buttons for actions
    ttk.Label(frame, text="Description:").grid(row=2, column=0, sticky=tk.W)
    description_entry = ttk.Entry(frame, width=20)
    description_entry.grid(row=2, column=1, sticky=tk.W)

    ttk.Label(frame, text="Amount:").grid(row=3, column=0, sticky=tk.W)
    amount_entry = ttk.Entry(frame, width=20)
    amount_entry.grid(row=3, column=1, sticky=tk.W)

    ttk.Label(frame, text="Category:").grid(row=4, column=0, sticky=tk.W)
    category_entry = ttk.Entry(frame, width=20)
    category_entry.grid(row=4, column=1, sticky=tk.W)

    # Add a section for updating the budget
    ttk.Label(frame, text="Update Budget:").grid(row=6, column=0, sticky=tk.W)
    budget_entry = ttk.Entry(frame, width=20)
    budget_entry.grid(row=6, column=1, sticky=tk.W)

    def update_budget_gui():
        nonlocal budget, initial_budget  # Ensure both variables are updated
        try:
            new_budget = float(budget_entry.get())
            budget = new_budget
            initial_budget = new_budget  # Update the initial_budget variable
            update_expenses_gui(expense_listbox, expenses, budget)
            budget_entry.delete(0, tk.END)
            messagebox.showinfo("Success", "Budget updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for the budget.")



    def add_expense_gui():
        description = description_entry.get()
        amount = float(amount_entry.get())
        category = category_entry.get()
        add_expense(expenses, description, amount, category)
        update_expenses_gui(expense_listbox, expenses, budget)
        description_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)

    def update_expense_gui():
        description = description_entry.get()
        new_description = description_entry.get()
        new_amount = float(amount_entry.get())
        if update_expense(expenses, description, new_description, new_amount):
            update_expenses_gui(expense_listbox, expenses, budget)
        else:
            messagebox.showerror("Error", "Expense not found!")
        description_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)

    def remove_expense_gui():
        description = description_entry.get()
        if remove_expense(expenses, description):
            update_expenses_gui(expense_listbox, expenses, budget)
        else:
            messagebox.showerror("Error", "Expense not found!")
        description_entry.delete(0, tk.END)

    def save_and_exit():
        save_budget_data(filepath, initial_budget, expenses)
        root.destroy()

    ttk.Button(frame, text="Add Expense", command=add_expense_gui).grid(row=5, column=0, sticky=tk.W)
    ttk.Button(frame, text="Update Expense", command=update_expense_gui).grid(row=5, column=1, sticky=tk.W)
    ttk.Button(frame, text="Remove Expense", command=remove_expense_gui).grid(row=5, column=2, sticky=tk.W)
    ttk.Button(frame, text="Update Budget", command=update_budget_gui).grid(row=6, column=2, sticky=tk.W)
    ttk.Button(frame, text="Save and Exit", command=save_and_exit).grid(row=7, column=3, sticky=tk.W)

    # Run the Tkinter main loop
    root.mainloop()


if __name__ == "__main__":
    main()