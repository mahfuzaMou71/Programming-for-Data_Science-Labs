

import os
import sys

try:
    import tkinter as tk
    from tkinter import messagebox
except ImportError:
    print("Tkinter is not installed. On Ubuntu/Debian run: sudo apt install python3-tk")
    sys.exit(1)

from gui import CampusCashApp
from manager import ExpenseManager

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expenses.json")


def main():
    manager = ExpenseManager(DATA_FILE)
    warnings = manager.load()               

    root = tk.Tk()
    CampusCashApp(root, manager)
    if warnings:
        messagebox.showwarning("Data file notice", "\n".join(warnings))
    root.mainloop()


if __name__ == "__main__":
    main()
