"""validation.py - input checking functions.

"""

import datetime

from models import CATEGORIES

MAX_AMOUNT = 1_000_000
MAX_NOTE_LENGTH = 50


def validate_amount(text):
    """Return the amount as a number, or raise ValueError."""
    text = str(text).strip()
    if text == "":
        raise ValueError("Amount is required.")
    try:
        amount = float(text)
    except ValueError:
        raise ValueError("Amount must be a number, for example 250 or 99.50.") from None
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if amount > MAX_AMOUNT:
        raise ValueError(f"Amount is too large (maximum {MAX_AMOUNT:,}).")
    return round(amount, 2)


def validate_date(text):
    """Return the date as 'YYYY-MM-DD', or raise ValueError."""
    text = str(text).strip()
    try:
        date = datetime.datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Date must look like 2026-10-18 (YYYY-MM-DD).") from None
    if date > datetime.date.today():
        raise ValueError("Date cannot be in the future.")
    return date.isoformat()


def validate_category(text):
    """Return the category if it is in the CATEGORIES tuple, or raise ValueError."""
    if text not in CATEGORIES:
        raise ValueError("Please choose a category from the list.")
    return text


def validate_note(text):
    """Return the note, or raise ValueError if it is too long."""
    text = str(text).strip()
    if len(text) > MAX_NOTE_LENGTH:
        raise ValueError(f"Note is too long (maximum {MAX_NOTE_LENGTH} characters).")
    return text
