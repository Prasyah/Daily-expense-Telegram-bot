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
- **`/exp amount category description [date]`** - Log a new expense
- Optional date parameter (1-31) defaults to today
- Example: `/exp 15000 Lunch Ayam 11`
- Supported categories: Bills, Expense, Reimbursement
- Automatically creating new sheet on first input on new month

### ✏️ Edit Expense
- **`/edit ID amount category description`** - Edit an existing expense using its ID
- Example: `/edit 3 20000 Lunch Gado2`

### 🗑️ Delete Expense
- **`/delete ID`** - Delete an expense using its ID
- Example: `/delete 3`

### 📊 Budget Status
- **`/budget`** - View remaining budget for the month
- Shows daily safe spending recommendations

### 📅 Daily Report
- **`/detail`** - View all expenses for today
- **`/detail date`** - View expenses for a specific date
- Example: `/detail 11` (shows all expenses on the 11th)

### 📆 Monthly Report
- **`/month month_year`** - View detailed monthly expense report
- Shows breakdown by category (Bills, Expense, Reimbursement)
- Example: `/month February_2026`

### ℹ️ Help
- **`/help`** - Display all available commands and usage examples

## Files

- [core.py](core.py): shared config and Google Sheets helpers
- [main.py](main.py): registers command handlers and runs the bot
-- `start.py` (top-level): starts the bot
-- Command modules moved into the `Feature` package: `Feature/income.py`, `Feature/exp.py`, `Feature/delete.py`, `Feature/edit.py`, `Feature/budget.py`, `Feature/detail.py`, `Feature/month.py`, `Feature/help.py`

