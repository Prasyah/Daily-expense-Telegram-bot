import telegram
from telegram.ext import ContextTypes
import pandas as pd

import core


async def month(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        sheet_name = context.args[0]

        sheet = core.spreadsheet.worksheet(sheet_name)

        data = sheet.get("A2:F1000")

        if not data:
            await update.message.reply_text("No data")
            return

        df = pd.DataFrame(
            data,
            columns=[
                "Date",
                "Time",
                "Amount",
                "Category",
                "Description"
            ]
        )

        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)

        bills = df[df["Category"].isin(core.BILLS)]["Amount"].sum()
        expense = df[df["Category"].isin(core.EXPENSE)]["Amount"].sum()
        reimb = df[df["Category"].isin(core.REIMBURSEMENT)]["Amount"].sum()
        total = bills + expense + reimb

        category_sum = df.groupby("Category")["Amount"].sum()

        text = (
            f"📊 Monthly Report ({sheet_name})\n\n"
            f"Bills: Rp{int(bills):,}\n"
            f"Expense: Rp{int(expense):,}\n"
            f"Reimbursement: Rp{int(reimb):,}\n\n"
            f"Total: Rp{int(total):,}\n\n"
            f"📂 Category Breakdown\n\n"
        )

        for cat, amt in category_sum.items():
            text += f"{cat}: Rp{int(amt):,}\n"

        await update.message.reply_text(text)

    except:
        await update.message.reply_text(
            "Usage:\n"
            "/month 02_2026"
        )
