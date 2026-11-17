"""models.py - the data model: the category tuple and the Expense class."""


CATEGORIES = ("Food", "Transport", "Books", "Rent", "Entertainment", "Other")


class Expense:
    """One spending record (the main data entity of the program)."""

    def __init__(self, expense_id, date, category, amount, note=""):
        self.expense_id = expense_id    
        self.date = date                
        self.category = category        
        self.amount = float(amount)    
        self.note = note                

    def to_dict(self):
        """Turn the object into a dictionary so it can be saved in a JSON file."""
        return {"id": self.expense_id, "date": self.date, "category": self.category,
                "amount": self.amount, "note": self.note}
