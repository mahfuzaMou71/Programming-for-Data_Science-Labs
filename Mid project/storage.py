"""storage.py - saving and loading (all file handling is here).

A missing or broken file never crashes the program.
"""

import json

from models import Expense


def load_expenses(path):
    """Read the JSON file. Returns (list of Expense, list of warning messages)."""
    expenses = []
    warnings = []
    used_ids = set()                       
    try:
        with open(path, "r", encoding="utf-8") as file:
            records = json.load(file)
    except FileNotFoundError:
        return expenses, ["No saved file found. Starting with an empty list."]
    except (json.JSONDecodeError, OSError):
        return expenses, ["The data file could not be read. Starting with an empty list."]

    if not isinstance(records, list):
        return expenses, ["The data file has the wrong format. Starting with an empty list."]

    for record in records:                 
        try:
            expense = Expense(record["id"], record["date"], record["category"],
                              record["amount"], record.get("note", ""))
        except (KeyError, ValueError, TypeError, AttributeError):
            warnings.append("One damaged record in the file was skipped.")
            continue
        if expense.expense_id in used_ids:
            warnings.append(f"Duplicate ID {expense.expense_id} was skipped.")
            continue
        used_ids.add(expense.expense_id)
        expenses.append(expense)
    return expenses, warnings


def save_expenses(path, expenses):
    """Write all expenses to the file. Returns "" if saved, or an error message."""
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump([expense.to_dict() for expense in expenses], file, indent=2)
    except OSError:
        return "Could not save the file. Please close it in other programs and try again."
    return ""
