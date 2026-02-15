import gspread
import pytz
import calendar
from datetime import datetime
from gspread_formatting import format_cell_range, CellFormat, NumberFormat

from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

load_dotenv()

# =========================
# CONFIG
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME", "Daily expense")
TIMEZONE = "Asia/Jakarta"

# =========================
# CATEGORY
# =========================

BILLS = [
    "Residence",
    "Electricity"
]

EXPENSE = [
    "Lunch",
    "Snacks",
    "Transport",
    "Other",
    "Unimportant",
    "Health"
]

REIMBURSEMENT = [
    "Reimbursement"
]

ALL_CATEGORY = BILLS + EXPENSE + REIMBURSEMENT

# =========================
# GOOGLE AUTH
# =========================

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

# Path to service account JSON (adjust if needed)
SERVICE_ACCOUNT_FILE = r'D:\TeleBot Expense\daily-487502-e9fc5d174cd1.json'

creds = ServiceAccountCredentials.from_json_keyfile_name(
    SERVICE_ACCOUNT_FILE, scope)

client = gspread.authorize(creds)

spreadsheet = client.open(SPREADSHEET_NAME)


def get_sheet():
    now = datetime.now(pytz.timezone(TIMEZONE))

    name = now.strftime("%B_%Y")

    try:
        sheet = spreadsheet.worksheet(name)

    except Exception:
        sheet = spreadsheet.add_worksheet(
            title=name,
            rows="1000",
            cols="20"
        )

        setup_sheet(sheet)

    return sheet


def setup_sheet(sheet):
    sheet.update("A1:F1", [[
        "No",
        "Date",
        "Time",
        "Category",
        "Amount",
        "Description"
    ]])

    sheet.update("H1:K1", [[
        "Category",
        "Budget",
        "Expense",
        "Leftover"
    ]])

    sheet.update("H2:K11",
        [
            ["Residence", 1700000, '=SUMIF(D2:D1000;"Residence";E2:E1000)', '=I2-J2'],
            ["Electricity", 70000, '=SUMIF(D2:D1000;"Electricity";E2:E1000)', '=I3-J3'],
            ["Lunch", 1500000, '=SUMIF(D2:D1000;"Lunch";E2:E1000)', '=I4-J4'],
            ["Snacks", 200000, '=SUMIF(D2:D1000;"Snacks";E2:E1000)', '=I5-J5'],
            ["Transport", 180000, '=SUMIF(D2:D1000;"Transport";E2:E1000)', '=I6-J6'],
            ["Other", 230000, '=SUMIF(D2:D1000;"Other";E2:E1000)', '=I7-J7'],
            ["Health", 120000, '=SUMIF(D2:D1000;"Health";E2:E1000)', '=I8-J8'],
            ["Unimportant", 0, '=SUMIF(D2:D1000;"Unimportant";E2:E1000)', '=I9-J9'],
            ["Reimbursement", 0, '=SUMIF(D2:D1000;"Reimbursement";E2:E1000)', '=I10-J10'],
            ["Total", 4000000, '=SUM(E2:E15)', '=SUM(K2:K10)']
        ],
        value_input_option="USER_ENTERED"
    )

    sheet.update("H13:H14", [
        ["Income"],
        ["Clean Income"]
    ])

    sheet.update("I14", [["=I13-J11"]], value_input_option="USER_ENTERED")

    # FORMAT RUPIAH
    rupiah_format = CellFormat(
        numberFormat=NumberFormat(
            type="CURRENCY",
            pattern="Rp#,##0"
        )
    )

    # Rupiah format column Amount in expense
    format_cell_range(sheet, "D2:D1000", rupiah_format)

    # Rupiah format column Budget, Expense, Leftover in budget
    format_cell_range(sheet, "I2:I14", rupiah_format)
    format_cell_range(sheet, "J2:J11", rupiah_format)
    format_cell_range(sheet, "K2:K11", rupiah_format)
