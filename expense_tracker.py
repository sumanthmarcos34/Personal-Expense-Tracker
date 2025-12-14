"""
CSV columns:
id,date,amount,category,description
"""

from __future__ import annotations
import csv
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Tuple

CSV_FILE = Path("expenses.csv")
DATE_FORMAT = "%Y-%m-%d"  #date format


@dataclass
class Expense:
    id: int
    date: str           #YYYY-MM-DD
    amount: float
    category: str
    description: str

    @property
    def date_obj(self) -> datetime:
        return datetime.strptime(self.date, DATE_FORMAT)


# ---------------------
# CSV utilities
# ---------------------
def ensure_csv_exists(path: Path = CSV_FILE) -> None:
    if not path.exists():
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "date", "amount", "category", "description"])
            writer.writeheader()


def read_all_expenses(path: Path = CSV_FILE) -> List[Expense]:
    ensure_csv_exists(path)
    expenses: List[Expense] = []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                expenses.append(Expense(
                    id=int(row["id"]),
                    date=row["date"],
                    amount=float(row["amount"]),
                    category=row["category"],
                    description=row["description"],
                ))
            except Exception:
                # Skip malformed rows
                continue
    return expenses


def write_expense(expense: Expense, path: Path = CSV_FILE) -> None:
    ensure_csv_exists(path)
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "date", "amount", "category", "description"])
        writer.writerow({
            "id": expense.id,
            "date": expense.date,
            "amount": f"{expense.amount:.2f}",
            "category": expense.category,
            "description": expense.description,
        })


def next_id(expenses: List[Expense]) -> int:
    if not expenses:
        return 1
    return max(e.id for e in expenses) + 1


# ---------------------
# Business logic
# ---------------------
def add_expense_interactive() -> None:
    expenses = read_all_expenses()
    eid = next_id(expenses)

    # Date
    while True:
        dt_in = input(f"Date (YYYY-MM-DD) [default: today]: ").strip()
        if dt_in == "":
            date_str = datetime.today().strftime(DATE_FORMAT)
            break
        try:
            _ = datetime.strptime(dt_in, DATE_FORMAT)
            date_str = dt_in
            break
        except ValueError:
            print(f"Invalid date format. Please use {DATE_FORMAT}.")

    # Amount
    while True:
        amt_txt = input("Amount (positive number): ").strip()
        try:
            amt = float(amt_txt)
            if amt <= 0:
                raise ValueError()
            break
        except Exception:
            print("Enter a valid positive number for amount.")

    # Category and description
    category = input("Category (e.g., groceries, transport, rent): ").strip() or "uncategorized"
    description = input("Description (optional): ").strip()

    exp = Expense(id=eid, date=date_str, amount=amt, category=category, description=description)
    write_expense(exp)
    print(f"Saved expense #{exp.id}: {exp.date} {exp.amount:.2f} {exp.category} — {exp.description}")


def list_expenses(limit: Optional[int] = None) -> None:
    expenses = read_all_expenses()
    expenses.sort(key=lambda e: e.date_obj, reverse=True)
    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"\nShowing {len(expenses) if limit is None else min(limit, len(expenses))} expenses (most recent first):")
    print("-" * 72)
    print(f"{'ID':>3}  {'Date':10}  {'Amount':>10}  {'Category':20}  Description")
    print("-" * 72)
    for i, e in enumerate(expenses):
        if limit is not None and i >= limit:
            break
        print(f"{e.id:>3}  {e.date:10}  {e.amount:10.2f}  {e.category:20}  {e.description}")
    print("-" * 72)


def summary_by_month() -> None:
    expenses = read_all_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return
    # Group by YYYY-MM
    totals: Dict[str, float] = {}
    counts: Dict[str, int] = {}
    for e in expenses:
        key = e.date_obj.strftime("%Y-%m")
        totals[key] = totals.get(key, 0.0) + e.amount
        counts[key] = counts.get(key, 0) + 1

    # Sort months descending
    items = sorted(totals.items(), key=lambda x: x[0], reverse=True)
    print("\nMonthly summary:")
    print("-" * 40)
    print(f"{'Month':7}  {'Total':>12}  {'Count':>6}  {'Average':>10}")
    print("-" * 40)
    for month, total in items:
        cnt = counts[month]
        avg = total / cnt if cnt else 0.0
        print(f"{month:7}  {total:12.2f}  {cnt:6d}  {avg:10.2f}")
    print("-" * 40)


def summary_by_category() -> None:
    expenses = read_all_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return
    totals: Dict[str, float] = {}
    counts: Dict[str, int] = {}
    for e in expenses:
        cat = e.category.strip().lower() or "uncategorized"
        totals[cat] = totals.get(cat, 0.0) + e.amount
        counts[cat] = counts.get(cat, 0) + 1

    items = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    total_all = sum(totals.values())
    print("\nCategory summary (descending by amount):")
    print("-" * 60)
    print(f"{'Category':20}  {'Total':>12}  {'Count':>6}  {'Percent':>10}")
    print("-" * 60)
    for cat, total in items:
        cnt = counts[cat]
        pct = (total / total_all * 100) if total_all else 0.0
        print(f"{cat:20}  {total:12.2f}  {cnt:6d}  {pct:9.2f}%")
    print("-" * 60)


def highest_and_lowest(n: int = 1) -> None:
    expenses = read_all_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return
    sorted_by_amount = sorted(expenses, key=lambda e: e.amount, reverse=True)
    top = sorted_by_amount[:n]
    bottom = sorted_by_amount[-n:] if n <= len(sorted_by_amount) else sorted_by_amount[::-1]

    print(f"\nTop {n} highest expenses:")
    print("-" * 72)
    for e in top:
        print(f"#{e.id} {e.date} {e.amount:.2f} {e.category} — {e.description}")

    print(f"\nTop {n} lowest expenses:")
    print("-" * 72)
    for e in reversed(bottom):  # show smallest first
        print(f"#{e.id} {e.date} {e.amount:.2f} {e.category} — {e.description}")


def search_by_text(q: str) -> None:
    expenses = read_all_expenses()
    qlow = q.lower()
    found = [e for e in expenses if qlow in e.description.lower() or qlow in e.category.lower()]
    if not found:
        print(f"No expenses matching '{q}'.")
        return
    found.sort(key=lambda e: e.date_obj, reverse=True)
    print(f"\nFound {len(found)} matching expenses:")
    for e in found:
        print(f"#{e.id} {e.date} {e.amount:.2f} {e.category} — {e.description}")


def export_csv(dst: str) -> None:
    src = CSV_FILE
    if not src.exists():
        print("No data to export.")
        return
    dstp = Path(dst).expanduser()
    with src.open("r", encoding="utf-8") as fsrc, dstp.open("w", encoding="utf-8") as fdst:
        fdst.write(fsrc.read())
    print(f"Exported CSV to {dstp}")


# ---------------------
# CLI menu
# ---------------------
def print_menu() -> None:
    print("\nPersonal Expense Tracker — Menu")
    print("1) Add expense")
    print("2) List recent expenses")
    print("3) Show monthly summary")
    print("4) Show category summary")
    print("5) Show highest / lowest spending")
    print("6) Search by text (category or description)")
    print("7) Export CSV copy")
    print("0) Exit")


def main_loop() -> None:
    ensure_csv_exists()
    while True:
        print_menu()
        choice = input("Choose option: ").strip()
        if choice == "1":
            add_expense_interactive()
        elif choice == "2":
            try:
                lim = int(input("How many recent? [Enter for all]: ") or "0")
                lim = None if lim == 0 else lim
            except ValueError:
                lim = None
            list_expenses(limit=lim)
        elif choice == "3":
            summary_by_month()
        elif choice == "4":
            summary_by_category()
        elif choice == "5":
            try:
                n = int(input("How many top entries? [default 1]: ") or "1")
                n = max(1, n)
            except ValueError:
                n = 1
            highest_and_lowest(n=n)
        elif choice == "6":
            q = input("Search query (text): ").strip()
            if q:
                search_by_text(q)
            else:
                print("Empty query.")
        elif choice == "7":
            dst = input("Export destination filename [e.g. backup.csv]: ").strip() or "expenses_backup.csv"
            export_csv(dst)
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Pick from the menu.")


if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\nExiting (keyboard interrupt). Bye.")
        sys.exit(0)
