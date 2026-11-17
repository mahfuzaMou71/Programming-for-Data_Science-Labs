"""analysis.py - calculation functions that use NumPy."""

import numpy as np


def basic_stats(amounts):
    """Return count, total, mean, largest and smallest (NumPy does the work)."""
    if len(amounts) == 0:
        return {"count": 0, "total": 0.0, "mean": 0.0, "max": 0.0, "min": 0.0}
    values = np.array(amounts, dtype=float)
    return {
        "count": int(values.size),
        "total": float(np.sum(values)),
        "mean": float(np.mean(values)),
        "max": float(np.max(values)),
        "min": float(np.min(values)),
    }


def category_totals(expenses):
    """Return a dictionary {category: total spent}."""
    totals = {}
    for expense in expenses:
        totals[expense.category] = totals.get(expense.category, 0.0) + expense.amount
    return totals


def category_percentages(totals):
    """Return {category: share of all spending in percent}, using a NumPy array."""
    if not totals:
        return {}
    names = list(totals.keys())
    values = np.array([totals[name] for name in names], dtype=float)
    shares = values / np.sum(values) * 100          # all percentages in one step
    return {name: round(float(share), 1) for name, share in zip(names, shares)}
