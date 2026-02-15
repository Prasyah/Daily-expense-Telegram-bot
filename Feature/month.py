import telegram
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import pandas as pd
from datetime import datetime

import core


async def month(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Get all worksheets
        worksheets = core.spreadsheet.worksheets()
        
        # Filter and sort worksheet titles (excluding the first default sheet if needed)
        sheet_names = [ws.title for ws in worksheets if ws.title]
        sheet_names.sort(reverse=True)
        
        # Get the latest 5 months
        latest_months = sheet_names[:5]
        
        if not latest_months:
            await update.message.reply_text("No monthly data available")
            return
        
        # Create inline buttons for month selection
        buttons = []
        for month_name in latest_months:
            buttons.append([
                InlineKeyboardButton(
                    text=month_name,
                    callback_data=f"month_{month_name}"
                )
            ])
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await update.message.reply_text(
            "📅 Select a month to view the report:",
            reply_markup=reply_markup
        )

    except Exception as e:
        await update.message.reply_text(
            "Usage:\n"
            "/month\n\n"
            "Shows the latest 5 months available"
        )


async def month_callback(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle month selection from inline buttons"""
    query = update.callback_query
    await query.answer()
    
    try:
        # Extract month name from callback data
        sheet_name = query.data.replace("month_", "")
        
        sheet = core.spreadsheet.worksheet(sheet_name)
        
        data = sheet.get("A2:F1000")
        
        if not data:
            await query.edit_message_text("No data for this month")
            return
        s
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
        
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)
        
        bills = df[df["Category"].isin(core.BILLS)]["Amount"].sum()
        expense = df[df["Category"].isin(core.EXPENSE)]["Amount"].sum()
        reimb = df[df["Category"].isin(core.REIMBURSEMENT)]["Amount"].sum()
        total = bills + expense + reimb
        
        category_sum = df.groupby("Category")["Amount"].sum()
        
        # Get budget information from the same sheet
        budgets_data = sheet.get("H2:I10")
        budget_dict = {}
        if budgets_data:
            for row in budgets_data:
                if len(row) >= 2:
                    try:
                        budget_dict[row[0]] = int(float(row[1])) if row[1] else 0
                    except:
                        budget_dict[row[0]] = 0
        
        text = (
            f"📊 Monthly Report ({sheet_name})\n\n"
            f"Bills: Rp{int(bills):,}\n"
            f"Expense: Rp{int(expense):,}\n"
            f"Reimbursement: Rp{int(reimb):,}\n\n"
            f"Total: Rp{int(total):,}\n\n"
            f"📂 Category Breakdown\n\n"
        )
        
        for cat, amt in category_sum.items():
            budget_amt = budget_dict.get(cat, 0)
            if budget_amt > 0:
                percentage = (amt / budget_amt) * 100
                text += f"{cat}: Rp{int(amt):,} ({percentage:.0f}%)\n"
            else:
                text += f"{cat}: Rp{int(amt):,}\n"
        
        await query.edit_message_text(text)
        
    except Exception as e:
        await query.edit_message_text(f"Error loading month data: {str(e)}")
