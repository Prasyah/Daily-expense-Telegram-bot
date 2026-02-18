import telegram
from telegram.ext import ContextTypes


async def help(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
╔═════════════════╗
  💰 DAILY EXPENSE BOT
╚═════════════════╝


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
• Telkom
• SF
• Sat
• XL
• Tri
• Other


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

/exp category description amount date(optional)

Example:
/exp Lunch Ayam 15000 11

Date optional → default today


━━━━━━━━━━━━━━━━━━

✏ Edit Expense

/edit ID category description amount date(optional)

Example:
/edit 3 Lunch Gado2 20000


━━━━━━━━━━━━━━━━━━

🗑 Delete Expense

/delete ID1 ID2 ID3 ...

Example:
/delete 3

Note: For reimbursements, use /reimburse delete


━━━━━━━━━━━━━━━━━━

💸 Reimbursement

Add reimbursement entry
/reimburse reimburse_category description amount date(optional)

Examples:
/reimburse Telkom ISP 300000 5
/reimburse SF Taxi 50000

Edit reimburse entry
/reimburse edit ID category description amount date(optional)

Delete reimburse entry (clears the row cells)
/reimburse delete ID1 ID2 ...

Show reimburse budgets and current expenses
/reimburse detail


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

/month


━━━━━━━━━━━━━━━━━━

✅ Tips

• Every expense has unique ID
• Use ID for edit/delete
• Budget auto calculated
• Currency auto Rupiah

━━━━━━━━━━━━━━━━━━
"""

    await update.message.reply_text(text)
