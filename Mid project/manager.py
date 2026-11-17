"""manager.py - ExpenseManager: keeps the records and does every operati
"""

import analysis
import storage
import validation
from models import Expense


class RecordNotFoundError(Exception):
    """when an expense ID does not exis"""


class ExpenseManager:
    def __init__(self, path):
        self.path = path
        self.expenses = []         
        self.used_ids = set()       
        self.last_error = ""        


    def load(self):
        """Load the saved data Returns a list of warning messages."""
        self.expenses, warnings = storage.load_expenses(self.path)
        self.used_ids = {expense.expense_id for expense in self.expenses}
        return warnings

    def save(self):
        self.last_error = storage.save_expenses(self.path, self.expenses)

    
    def make_id(self):
        """next free ID  E014."""
        number = len(self.expenses) + 1
        while f"E{number:03d}" in self.used_ids:
            number += 1
        return f"E{number:03d}"

    def add_expense(self, date_text, category_text, amount_text, note_text=""):
        """Check the input, add a new expense and save it."""
        date = validation.validate_date(date_text)
        category = validation.validate_category(category_text)
        amount = validation.validate_amount(amount_text)
        note = validation.validate_note(note_text)

        expense = Expense(self.make_id(), date, category, amount, note)
        self.expenses.append(expense)
        self.used_ids.add(expense.expense_id)
        self.save()
        return expense

    def find_by_id(self, expense_id):
        """Return the expense with this ID or raise RecordNotFoundError."""
        for expense in self.expenses:
            if expense.expense_id == expense_id:
                return expense
        raise RecordNotFoundError(f"No expense with ID {expense_id} was found.")

    def change_amount(self, expense_id, amount_text):
        """Change the amount of an existing expense."""
        amount = validation.validate_amount(amount_text)
        expense = self.find_by_id(expense_id)
        expense.amount = amount
        self.save()
        return expense

    def delete_expense(self, expense_id):
        """Remove an expense."""
        expense = self.find_by_id(expense_id)
        self.expenses.remove(expense)
        self.used_ids.discard(expense_id)
        self.save()

    def search(self, category="All"):
        """Return the expenses of one category newest first."""
        results = []
        for expense in self.expenses:
            if category == "All" or expense.category == category:
                results.append(expense)
        results.sort(key=lambda e: e.date, reverse=True)
        return results

    # ------------------------------------------------------------ summary
    def summary_text(self):
        """Build the summary shown on the Summary tab."""
        if not self.expenses:
            return "No expenses yet."
        stats = analysis.basic_stats([e.amount for e in self.expenses])
        totals = analysis.category_totals(self.expenses)
        percents = analysis.category_percentages(totals)

        lines = [
            f"Number of expenses : {stats['count']}",
            f"Total spent        : {stats['total']:,.2f}",
            f"Average expense    : {stats['mean']:,.2f}",
            f"Largest expense    : {stats['max']:,.2f}",
            f"Smallest expense   : {stats['min']:,.2f}",
            "",
            "Spending by category",
        ]
        ranked = sorted(totals.items(), key=lambda pair: pair[1], reverse=True)
        for category, total in ranked:
            lines.append(f"  {category:<14}{total:>12,.2f}   {percents[category]:5.1f}%")

        top = ranked[0][0]
        lines.append("")
        if percents[top] > 50:
            lines.append(f"Warning: more than half of your money went on {top}.")
        else:
            lines.append(f"Your biggest spending category is {top}.")
        return "\n".join(lines)
