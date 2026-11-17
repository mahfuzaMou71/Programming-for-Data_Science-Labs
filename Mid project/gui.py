"""gui.py - the Tkinter window (the interface functions).

This file only draws the window and reacts to buttons. All rules, calculations
and file work are done by ExpenseManager.
"""

import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from manager import RecordNotFoundError
from models import CATEGORIES


class CampusCashApp:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager
        root.title("CampusCash Lite - Student Expense Tracker")
        root.geometry("760x560")

        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(root, textvariable=self.status_var, relief="sunken",
                  anchor="w", padding=4).pack(side="bottom", fill="x")

        tabs = ttk.Notebook(root)
        tabs.pack(fill="both", expand=True, padx=8, pady=8)
        self.expenses_tab = ttk.Frame(tabs, padding=10)
        self.summary_tab = ttk.Frame(tabs, padding=10)
        tabs.add(self.expenses_tab, text="Expenses")
        tabs.add(self.summary_tab, text="Summary")

        self.build_expenses_tab()
        self.build_summary_tab()
        self.refresh_all()

    # ------------------------------------------------------ Expenses tab
    def build_expenses_tab(self):
        frame = self.expenses_tab

        # --- form to add an expense
        form = ttk.LabelFrame(frame, text="Add a new expense", padding=8)
        form.pack(fill="x")
        self.date_var = tk.StringVar(value=datetime.date.today().isoformat())
        self.category_var = tk.StringVar(value=CATEGORIES[0])
        self.amount_var = tk.StringVar()
        self.note_var = tk.StringVar()

        ttk.Label(form, text="Date (YYYY-MM-DD)").grid(row=0, column=0, sticky="w", pady=3)
        ttk.Entry(form, textvariable=self.date_var, width=16).grid(row=0, column=1, padx=6)
        ttk.Label(form, text="Category").grid(row=0, column=2, sticky="w")
        ttk.Combobox(form, textvariable=self.category_var, values=CATEGORIES,
                     state="readonly", width=14).grid(row=0, column=3, padx=6)
        ttk.Label(form, text="Amount").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Entry(form, textvariable=self.amount_var, width=16).grid(row=1, column=1, padx=6)
        ttk.Label(form, text="Note (optional)").grid(row=1, column=2, sticky="w")
        ttk.Entry(form, textvariable=self.note_var, width=30).grid(row=1, column=3, padx=6)
        ttk.Button(form, text="Add Expense", command=self.add_expense).grid(
            row=0, column=4, rowspan=2, padx=10)

        # --- search by category
        search = ttk.Frame(frame)
        search.pack(fill="x", pady=8)
        self.filter_var = tk.StringVar(value="All")
        ttk.Label(search, text="Show category:").pack(side="left")
        ttk.Combobox(search, textvariable=self.filter_var, values=("All",) + CATEGORIES,
                     state="readonly", width=14).pack(side="left", padx=6)
        ttk.Button(search, text="Search", command=self.refresh_table).pack(side="left")

        # --- table of expenses
        columns = ("id", "date", "category", "amount", "note")
        table = ttk.Frame(frame)
        table.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(table, columns=columns, show="headings", selectmode="browse")
        for column, title, width in (("id", "ID", 60), ("date", "Date", 100),
                                     ("category", "Category", 110), ("amount", "Amount", 100),
                                     ("note", "Note", 280)):
            self.tree.heading(column, text=title)
            self.tree.column(column, width=width)
        scrollbar = ttk.Scrollbar(table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- buttons under the table
        buttons = ttk.Frame(frame)
        buttons.pack(fill="x", pady=(8, 0))
        ttk.Button(buttons, text="Change Amount", command=self.change_amount).pack(side="left")
        ttk.Button(buttons, text="Delete Selected", command=self.delete_selected).pack(
            side="left", padx=8)

    def add_expense(self):
        try:
            expense = self.manager.add_expense(self.date_var.get(), self.category_var.get(),
                                               self.amount_var.get(), self.note_var.get())
        except ValueError as error:                       # a validation message
            messagebox.showerror("Invalid input", str(error))
            return
        self.amount_var.set("")
        self.note_var.set("")
        self.after_change(f"Saved as {expense.expense_id}.")

    def selected_id(self):
        """Return the ID of the selected row, or None (with a message)."""
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("No selection", "Please click an expense in the table first.")
            return None
        return selection[0]

    def change_amount(self):
        expense_id = self.selected_id()
        if expense_id is None:
            return
        new_amount = simpledialog.askstring("Change amount", f"New amount for {expense_id}:")
        if new_amount is None:                            # the user pressed Cancel
            return
        try:
            self.manager.change_amount(expense_id, new_amount)
        except ValueError as error:
            messagebox.showerror("Invalid input", str(error))
            return
        except RecordNotFoundError as error:
            messagebox.showerror("Not found", str(error))
            self.refresh_all()
            return
        self.after_change(f"Updated {expense_id}.")

    def delete_selected(self):
        expense_id = self.selected_id()
        if expense_id is None:
            return
        if not messagebox.askyesno("Delete", f"Delete expense {expense_id}?"):
            return
        try:
            self.manager.delete_expense(expense_id)
        except RecordNotFoundError as error:
            messagebox.showerror("Not found", str(error))
            self.refresh_all()
            return
        self.after_change(f"Deleted {expense_id}.")

    def refresh_table(self):
        results = self.manager.search(self.filter_var.get())
        self.tree.delete(*self.tree.get_children())
        for expense in results:
            self.tree.insert("", "end", iid=expense.expense_id, values=(
                expense.expense_id, expense.date, expense.category,
                f"{expense.amount:,.2f}", expense.note))
        self.status_var.set(f"{len(results)} of {len(self.manager.expenses)} expenses shown.")

    # ------------------------------------------------------- Summary tab
    def build_summary_tab(self):
        ttk.Button(self.summary_tab, text="Refresh Summary",
                   command=self.refresh_summary).pack(anchor="w", pady=(0, 8))
        self.summary_box = tk.Text(self.summary_tab, height=20, font=("Courier", 11),
                                   state="disabled")
        self.summary_box.pack(fill="both", expand=True)

    def refresh_summary(self):
        self.summary_box.configure(state="normal")
        self.summary_box.delete("1.0", "end")
        self.summary_box.insert("1.0", self.manager.summary_text())
        self.summary_box.configure(state="disabled")

    # ------------------------------------------------------------ shared
    def refresh_all(self):
        self.refresh_table()
        self.refresh_summary()

    def after_change(self, message):
        """Runs after every add / change / delete."""
        if self.manager.last_error:
            messagebox.showerror("Save problem", self.manager.last_error)
        self.refresh_all()
        self.status_var.set(message)
