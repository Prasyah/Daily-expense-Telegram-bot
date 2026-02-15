# Daily Expense Bot

Simple Telegram bot that logs expenses to a Google Spreadsheet.

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

Files

- [core.py](core.py): shared config and Google Sheets helpers
- [main.py](main.py): registers command handlers and runs the bot
-- `start.py` (top-level): starts the bot
-- Command modules moved into the `Feature` package: `Feature/income.py`, `Feature/exp.py`, `Feature/delete.py`, `Feature/edit.py`, `Feature/budget.py`, `Feature/detail.py`, `Feature/month.py`, `Feature/help.py`
