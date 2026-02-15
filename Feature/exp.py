import telegram
from telegram.ext import ContextTypes
import pytz
from datetime import datetime

import core


async def exp(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        sheet = core.get_sheet()

        now = datetime.now(pytz.timezone(core.TIMEZONE))

        amount = int(context.args[0])

        category = context.args[1]

        if category not in core.ALL_CATEGORY:
            await update.message.reply_text("Invalid category")
            return

        last_arg = context.args[-1]

        if last_arg.isdigit() and 1 <= int(last_arg) <= 31:
            day = int(last_arg)
            description = " ".join(context.args[2:-1])
        else:
            day = now.day
            description = " ".join(context.args[2:])

        date_obj = now.replace(day=day)
        date = date_obj.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        no_list = sheet.col_values(1)

        if len(no_list) <= 1:
            next_no = 1
        else:
            next_no = int(no_list[-1]) + 1

        next_row = len(no_list) + 1

        sheet.update(
            f"A{next_row}:F{next_row}",
            [[
                next_no,
                date,
                time,
                category,
                amount,
                description
            ]],
            value_input_option="USER_ENTERED"
        )

        await update.message.reply_text(f"Saved with ID {next_no}")

    except Exception:
        await update.message.reply_text(
            "Usage:\n"
            "/exp amount category description date(optional)\n"
            "Bills: Residence, electricity\n"
            "Expense: Lunch, Snacks, Transport, Other, Unimportant, Health\n"
            "Reimbursement: Reimbursement\n"
        )
