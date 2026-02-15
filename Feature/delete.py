import telegram
from telegram.ext import ContextTypes

import core


async def delete(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        target_id = int(context.args[0])
        sheet = core.get_sheet()
        ids = sheet.col_values(1)
        row = ids.index(str(target_id)) + 1
        sheet.delete_rows(row)
        await update.message.reply_text(f"Deleted ID {target_id}")
    except:
        await update.message.reply_text("Usage:\n/delete ID")
