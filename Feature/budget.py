import telegram
from telegram.ext import ContextTypes
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import calendar
from datetime import datetime

import core


async def budget(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        sheet = core.get_sheet()
        categories = sheet.get("H2:H10")
        
        if not categories:
            await update.message.reply_text("No categories available")
            return
        
        # Create inline buttons for category selection
        buttons = []
        
        # Add All button
        buttons.append([
            InlineKeyboardButton(
                text="📊 All Categories",
                callback_data="budget_all"
            )
        ])
        
        # Add category buttons
        for category in categories:
            cat_name = category[0]
            buttons.append([
                InlineKeyboardButton(
                    text=cat_name,
                    callback_data=f"budget_{cat_name}"
                )
            ])
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await update.message.reply_text(
            "📊 Select a category to view budget details:",
            reply_markup=reply_markup
        )

    except Exception as e:
        await update.message.reply_text(
            "Usage:\n"
            "/budget\n\n"
            "Shows budget options for each category"
        )


async def budget_callback(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle category selection from inline buttons"""
    query = update.callback_query
    await query.answer()
    
    try:
        sheet = core.get_sheet()

        categories = sheet.get("H2:H10")
        budgets = sheet.get("I2:I10", value_render_option="UNFORMATTED_VALUE")
        expenses = sheet.get("J2:J10", value_render_option="UNFORMATTED_VALUE")
        leftover = sheet.get("K2:K10", value_render_option="UNFORMATTED_VALUE")

        now = datetime.now()
        today = now.day
        days_in_month = calendar.monthrange(now.year, now.month)[1]
        days_left = days_in_month - today
        if days_left == 0:
            days_left = 1

        selected_category = query.data.replace("budget_", "")

        text = "📊 Budget Status\n\n"
        
        total_budget = 0
        total_used = 0

        if selected_category == "all":
            # Show all categories
            for i in range(len(categories)):
                cat = categories[i][0]
                try:
                    budget_amt = int(float(budgets[i][0])) if budgets[i][0] else 0
                    expense_amt = int(float(expenses[i][0])) if expenses[i][0] else 0
                    left = int(float(leftover[i][0])) if leftover[i][0] else 0
                except:
                    budget_amt = 0
                    expense_amt = 0
                    left = 0
                
                total_budget += budget_amt
                total_used += expense_amt
                
                # Calculate percentage
                if budget_amt > 0:
                    percentage = (expense_amt / budget_amt) * 100
                    percentage_str = f" ({percentage:.0f}%)"
                else:
                    percentage_str = " (N/A)"

                if cat == "Lunch":
                    per_day = left // days_left if left > 0 else 0
                    text += (
                        f"{cat}\n"
                        f"Budget: Rp{budget_amt:,}\n"
                        f"Used: Rp{expense_amt:,}{percentage_str}\n"
                        f"Left: Rp{left:,}\n"
                        f"Per day: Rp{per_day:,}\n\n"
                    )
                else:
                    text += (
                        f"{cat}\n"
                        f"Budget: Rp{budget_amt:,}\n"
                        f"Used: Rp{expense_amt:,}{percentage_str}\n"
                        f"Left: Rp{left:,}\n\n"
                    )
            
            # Add total summary
            if total_budget > 0:
                total_percentage = (total_used / total_budget) * 100
            else:
                total_percentage = 0
            
            text += (
                f"━━━━━━━━━━━━━━━━━\n"
                f"📌 Total\n"
                f"Budget: Rp{total_budget:,}\n"
                f"Used: Rp{total_used:,} ({total_percentage:.0f}%)\n"
            )
        else:
            # Show specific category
            for i in range(len(categories)):
                if categories[i][0] == selected_category:
                    cat = categories[i][0]
                    try:
                        budget_amt = int(float(budgets[i][0])) if budgets[i][0] else 0
                        expense_amt = int(float(expenses[i][0])) if expenses[i][0] else 0
                        left = int(float(leftover[i][0])) if leftover[i][0] else 0
                    except:
                        budget_amt = 0
                        expense_amt = 0
                        left = 0
                    
                    # Calculate percentage
                    if budget_amt > 0:
                        percentage = (expense_amt / budget_amt) * 100
                        percentage_str = f" ({percentage:.0f}%)"
                    else:
                        percentage_str = " (N/A)"

                    text += (
                        f"{cat}\n"
                        f"Budget: Rp{budget_amt:,}\n"
                        f"Used: Rp{expense_amt:,}{percentage_str}\n"
                        f"Left: Rp{left:,}\n"
                    )
                    
                    if cat == "Lunch":
                        per_day = left // days_left if left > 0 else 0
                        text += f"Per day: Rp{per_day:,}\n"
                    break
        
        await query.edit_message_text(text)
        
    except Exception as e:
        await query.edit_message_text(f"Error loading budget data: {str(e)}")
