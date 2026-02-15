import telegram
from telegram.ext import ContextTypes


async def help(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
╔══════════════════════╗
💰 DAILY EXPENSE BOT
╚══════════════════════╝


📂 CATEGORY

🏠 Bills
• Residence
• Electricity

🍽 Expense
• Lunch
• Snacks
• Transport
• Other
• Unimportant
• Health

🔁 Reimbursement
• Reimbursement


━━━━━━━━━━━━━━━━━━
📌 COMMAND LIST
━━━━━━━━━━━━━━━━━━


💵 Income

Show clean income
/income

Add income
/income amount

Example:
/income 500000


━━━━━━━━━━━━━━━━━━

💸 Add Expense

/exp amount category description date(optional)

Example:
/exp 15000 Lunch Ayam 11

Date optional → default today


━━━━━━━━━━━━━━━━━━

✏ Edit Expense

/edit ID amount category description

Example:
/edit 3 20000 Lunch Gado2


━━━━━━━━━━━━━━━━━━

🗑 Delete Expense

/delete ID

Example:
/delete 3


━━━━━━━━━━━━━━━━━━

📊 Budget Status

/budget

Show remaining budget
and daily safe spending


━━━━━━━━━━━━━━━━━━

📅 Daily Report

/detail

/detail date

Example:
/detail 11


━━━━━━━━━━━━━━━━━━

📆 Monthly Report

/month month_year

Example:
/month February_2026


━━━━━━━━━━━━━━━━━━

✅ Tips

• Every expense has unique ID
• Use ID for edit/delete
• Budget auto calculated
• Currency auto Rupiah
"""

    await update.message.reply_text(text)
