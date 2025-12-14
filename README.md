# Personal Expense Tracker

A Python-based command-line application that helps users track daily expenses, store them in a CSV file, and generate basic spending reports.

--> Features

* Add daily expenses with date, category, amount, and description
* Store all expense data persistently in a CSV file
* Generate monthly expense summaries
* Generate category-wise expense summaries
* Identify highest and lowest spending entries
* Simple and user-friendly command-line interface
* Clean and modular code structure

------------------------------------------------------------------------

--> Technologies Used

* Python 3
* CSV file handling
* Command Line Interface (CLI)

------------------------------------------------------------------------

--> Project Structure

personal-expense-tracker/
  - expense_tracker.py
  - expenses.csv
  - README.md

------------------------------------------------------------------------

--> How to Run the Project

1. Clone the repository

  git clone https://github.com/sumanthmarcos34/personal-expense-tracker.git

2. Navigate to the project directory

  cd personal-expense-tracker

3. Run the application

  python expense_tracker.py

---------------------------------------------------------------------------

--> Usage Instructions

After running the program you will see the following menu:

  Personal Expense Tracker — Menu
  1) Add expense
  2) List recent expenses
  3) Show monthly summary
  4) Show category summary
  5) Show highest / lowest spending
  6) Search by text (category or description)
  7) Export CSV copy
  0) Exit

---------------------------------------------------------------------------

1) Add Expense

Choose option 1 to add a new expense.

You will be prompted for:

* Date (YYYY-MM-DD). Press Enter to use today’s date.
* Amount (positive number only).
* Category (e.g., groceries, transport, rent).
* Description (optional).

Each expense is automatically assigned a unique ID and saved to expenses.csv.

-----------------------------------------------------------------------------------------

2) List Recent Expenses

Choose option 2 to view recorded expenses.

* You can specify how many recent entries to display.
* Press Enter to list all expenses.
* Expenses are shown in descending order by date.

------------------------------------------------------------------------------------------

3) Monthly Summary

Choose option 3 to view a month-wise expense report.

The summary displays:

* Month (YYYY-MM)
* Total amount spent
* Number of transactions
* Average expense per transaction

------------------------------------------------------------------------------------------

4) Category Summary

Choose option 4 to view spending grouped by category.

The summary shows:

* Category name
* Total amount spent
* Number of transactions
* Percentage contribution to total spending

Categories are displayed in descending order of total amount.

-------------------------------------------------------------------------------------------

5) Highest / Lowest Spending

Choose option 5 to identify extreme spending entries.

* Enter how many top entries you want (default is 1).
* Displays highest and lowest expenses with full details.

-------------------------------------------------------------------------------------------

6) Search by Text

Choose option 6 to search expenses.

* Enter a keyword to search in category or description.
* Matching expenses are displayed sorted by most recent date.

-------------------------------------------------------------------------------------------

7) Export CSV Copy

Choose option 7 to export a backup copy of the CSV file.

* Enter destination filename (example: 'backup.csv').
* If left empty, the file is saved as 'expenses_backup.csv'.

-------------------------------------------------------------------------------------------

8) Exit

Choose option 0 to safely exit the application.

--------------------------------------------------------------------------------------------

--> Data Storage

All expense data is stored persistently in : 'expenses.csv'

The CSV structure is : id,date,amount,category,description

-------------------------------------------------------------------------------------------

Sumanth R
