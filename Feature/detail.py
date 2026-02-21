import telegram
from telegram.ext import ContextTypes
import pandas as pd
import pytz
from datetime import datetime

import core


async def detail(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    sheet = core.get_sheet()
    data = sheet.get("A2:F1000")

    if not data:
        await update.message.reply_text("No data")
        return

    df = pd.DataFrame(
        data,
        columns=[
            "No",
            "Date",
            "Time",
            "Category",
            "Amount",
            "Description"
        ]
    )

    # Clean Amount column: remove "Rp" prefix and periods (thousand separators)
    df["Amount"] = df["Amount"].astype(str).str.replace("Rp", "").str.replace(".", "")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)

    now = datetime.now(pytz.timezone(core.TIMEZONE))

    if len(context.args) == 0:
        target_date = now.strftime("%Y-%m-%d")
    else:
        try:
            day = int(context.args[0])
            target_date = now.strftime(f"%Y-%m-{day:02d}")
        except:
            await update.message.reply_text(
                "Usage:\n"
                "/detail\n"
                "/detail 11"
            )
            return

    df_today = df[df["Date"] == target_date]

    if df_today.empty:
        await update.message.reply_text(f"No transaction on {target_date}")
        return

    bills = df_today[df_today["Category"].isin(core.BILLS)]["Amount"].sum()
    expense = df_today[df_today["Category"].isin(core.EXPENSE)]["Amount"].sum()
    reimb = df_today[df_today["Category"].isin(core.REIMBURSEMENT)]["Amount"].sum()
    total = bills + expense + reimb

    category_sum = df_today.groupby("Category")["Amount"].sum()

    text = (
        f"📊 Report ({target_date})\n\n"
        f"Bills: Rp{int(bills):,}\n"
        f"Expense: Rp{int(expense):,}\n"
        f"Reimbursement: Rp{int(reimb):,}\n\n"
        f"Total: Rp{int(total):,}\n\n"
        f"📂 Category Breakdown\n\n"
    )

    for cat, amt in category_sum.items():
        text += f"{cat}: Rp{int(amt):,}\n"

    text += "\n🧾 Transactions\n\n"

    for index, row in df_today.iterrows():
        text += (
            f"• {row['Time']} | {row['Category']} — Rp{int(row['Amount']):,}\n"
            f"  {row['Description']}\n\n"
        )

    await update.message.reply_text(text)
