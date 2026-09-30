import json
import os
from collections import defaultdict
import matplotlib.pyplot as plt

DEFAULT_CATEGORIES = [
    "Food", "Rent", "Transportation", "Entertainment", "Utilities", "Savings"
]

class Budget:
    def __init__(self, file_path):
        self.file_path = file_path
        self.balance = 0.0
        self.transactions = []
        self.categories = set(DEFAULT_CATEGORIES)
        self.load_data()

    def load_data(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r") as f:
                    data = json.load(f)
                    self.balance = float(data.get("balance", 0.0))
                    self.transactions = data.get("transactions", [])
                    self.categories = set(data.get("categories", DEFAULT_CATEGORIES))
        except (json.JSONDecodeError, ValueError, IOError):
            print("Error loading file. Starting with a fresh budget.")
            self.balance = 0.0
            self.transactions = []
            self.categories = set(DEFAULT_CATEGORIES)

    def save_data(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump({
                    "balance": self.balance,
                    "transactions": self.transactions,
                    "categories": list(self.categories)
                }, f, indent=4)
        except IOError:
            print("Error saving data.")

    def add_income(self, amount, description=""):
        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError

            self.balance += amount
            self.transactions.append({
                "type": "income",
                "amount": amount,
                "description": description
            })
            self.save_data()
            print(f"Added income: ${amount:.2f}")
        except ValueError:
            print("Invalid income amount.")

    def add_expense(self, amount, category, description=""):
        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError

            if category not in self.categories:
                print("Category not found. Adding it.")
                self.categories.add(category)

            self.balance -= amount
            self.transactions.append({
                "type": "expense",
                "amount": amount,
                "category": category,
                "description": description
            })
            self.save_data()
            print(f"Added expense: ${amount:.2f} ({category})")
        except ValueError:
            print("Invalid expense amount.")

    def add_category(self, category):
        if not category.strip():
            print("Category name cannot be empty.")
            return

        self.categories.add(category)
        self.save_data()
        print(f"Category '{category}' added.")

    def show_balance(self):
        print(f"\nCurrent Balance: ${self.balance:.2f}\n")

    def spending_summary(self):
        summary = defaultdict(float)
        for t in self.transactions:
            try:
                if t.get("type") == "expense":
                    summary[t.get("category", "Unknown")] += float(t.get("amount", 0))
            except (ValueError, TypeError):
                continue

        print("\nSpending Summary:")
        for cat, amt in summary.items():
            print(f"{cat}: ${amt:.2f}")
        print()

    def show_pie_chart(self):
        summary = defaultdict(float)
        for t in self.transactions:
            try:
                if t.get("type") == "expense":
                    summary[t.get("category", "Unknown")] += float(t.get("amount", 0))
            except (ValueError, TypeError):
                continue

        if not summary:
            print("No expenses to display.")
            return

        try:
            labels = list(summary.keys())
            sizes = list(summary.values())

            plt.figure(figsize=(6,6))
            plt.pie(sizes, labels=labels, autopct='%1.1f%%')
            plt.title("Expense Breakdown")
            plt.show()
        except Exception:
            print("Error displaying chart.")


def safe_input_float(prompt):
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid number.")


def choose_budget_file():
    while True:
        print("1. Create New Budget")
        print("2. Load Existing Budget")

        choice = input("Choose an option: ")

        if choice == "1":
            file_name = input("Enter new file name (e.g. my_budget.json): ")
            if not file_name.endswith(".json"):
                file_name += ".json"

            try:
                if not os.path.exists(file_name):
                    with open(file_name, "w") as f:
                        json.dump({
                            "balance": 0.0,
                            "transactions": [],
                            "categories": DEFAULT_CATEGORIES
                        }, f, indent=4)
                return file_name
            except IOError:
                print("Error creating file.")

        elif choice == "2":
            file_name = input("Enter file name to load: ")
            if os.path.exists(file_name):
                return file_name
            else:
                print("File not found.")

        else:
            print("Invalid choice.")


def menu():
    file_path = choose_budget_file()
    budget = Budget(file_path)

    while True:
        print("\n--- Budget Menu ---")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. Add Category")
        print("4. Show Balance")
        print("5. Spending Summary")
        print("6. Show Expense Pie Chart")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            amount = safe_input_float("Enter income amount: ")
            desc = input("Description (optional): ")
            budget.add_income(amount, desc)

        elif choice == "2":
            amount = safe_input_float("Enter expense amount: ")
            print("Categories:", ", ".join(budget.categories))
            category = input("Enter category: ")
            desc = input("Description (optional): ")
            budget.add_expense(amount, category, desc)

        elif choice == "3":
            category = input("Enter new category name: ")
            budget.add_category(category)

        elif choice == "4":
            budget.show_balance()

        elif choice == "5":
            budget.spending_summary()

        elif choice == "6":
            budget.show_pie_chart()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nProgram exited safely.")
