import telegram
from telegram.ext import ContextTypes

import core


async def edit(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        target_id = int(context.args[0])
        category = context.args[1]
        
        last_arg = context.args[-1]
        
        if last_arg.isdigit() and 1 <= int(last_arg) <= 31:
            day = int(last_arg)
            amount = int(context.args[-2])
            description = " ".join(context.args[2:-2])
        else:
            amount = int(context.args[-1])
            description = " ".join(context.args[2:-1])
            day = None

        sheet = core.get_sheet()
        ids = sheet.col_values(1)
        row = ids.index(str(target_id)) + 1

        sheet.update(f"D{row}", [[category]])
        sheet.update(f"E{row}", [[amount]])
        sheet.update(f"F{row}", [[description]])
        
        if day is not None:
            import pytz
            from datetime import datetime
            now = datetime.now(pytz.timezone("Asia/Jakarta"))
            date_obj = now.replace(day=day)
            date = date_obj.strftime("%Y-%m-%d")
            sheet.update(f"B{row}", [[date]])

        await update.message.reply_text(f"Updated ID {target_id}")
    except:
        await update.message.reply_text(
            "Usage:\n/edit ID category description amount date(optional)"
        )
