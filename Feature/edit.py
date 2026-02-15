import telegram
from telegram.ext import ContextTypes

import core


async def edit(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        target_id = int(context.args[0])
        amount = int(context.args[1])
        category = context.args[2]
        description = " ".join(context.args[3:])

        sheet = core.get_sheet()
        ids = sheet.col_values(1)
        row = ids.index(str(target_id)) + 1

        sheet.update(f"D{row}", [[category]])
        sheet.update(f"E{row}", [[amount]])
        sheet.update(f"F{row}", [[description]])

        await update.message.reply_text(f"Updated ID {target_id}")
    except:
        await update.message.reply_text(
            "Usage:\n/edit ID amount category description"
        )
