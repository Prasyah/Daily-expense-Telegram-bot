# Daily Expense Bot

Simple Telegram bot that logs expenses to a Google Spreadsheet.

Requirement : Python 3.12

Quickstart


1. Place your Google service account JSON into the project folder and update `core.SERVICE_ACCOUNT_FILE` in [core.py](core.py) if needed.

2. Create a `.env` file by copying `.env.example` and filling the values (or edit the provided `.env`). The bot reads `BOT_TOKEN` and `SPREADSHEET_NAME` from environment variables.

3. Install dependencies:

```bash
pip install python-telegram-bot gspread oauth2client gspread-formatting pandas python-dateutil pytz python-dotenv
```

4. Run the bot:

```bash
python main.py
```

## Features

### 💰 Income Management
- **`/income`** - Display your clean income
- **`/income amount`** - Save your income
- Example: `/income 500000`

### 💸 Add Expense
- **`/exp category description amount [date]`** - Log a new expense
- Optional date parameter (1-31) defaults to today
- Example: `/exp Lunch Ayam 15000 11`
- Supported categories: Bills, Expense, Reimbursement
- Automatically creating new sheet on first input on new month

### ✏️ Edit Expense
- **`/edit ID amount category description`** - Edit an existing expense using its ID
- Example: `/edit 3 20000 Lunch Gado2`

### 🗑️ Delete Expense
- **`/delete ID1 [ID2 ID3 ...]`** - Delete one or more expenses using their IDs
- Example: `/delete 3` or `/delete 41 42 43`

### 📊 Budget Status
- **`/budget`** - Display budget options as interactive buttons
- Choose "All Categories" to see complete budget status or select a specific category
- Shows budget, used amount, usage percentage, and remaining balance
- Shows daily safe spending recommendations
- Displays total budget and overall usage percentage when viewing all categories

### 📅 Daily Report
- **`/detail`** - View all expenses for today
- **`/detail date`** - View expenses for a specific date
- Example: `/detail 11` (shows all expenses on the 11th)

### 📆 Monthly Report
- **`/month`** - Display the last 5 months as interactive buttons
- Select a month to view detailed expense report
- Shows breakdown by category (Bills, Expense, Reimbursement)
- Displays usage percentage for each category compared to budget

### ℹ️ Help
- **`/help`** - Display all available commands and usage examples

## Files

- [core.py](core.py): shared config and Google Sheets helpers
- [main.py](main.py): registers command handlers and runs the bot
-- `start.py` (top-level): starts the bot
-- Command modules moved into the `Feature` package: `Feature/income.py`, `Feature/exp.py`, `Feature/delete.py`, `Feature/edit.py`, `Feature/budget.py`, `Feature/detail.py`, `Feature/month.py`, `Feature/help.py`

