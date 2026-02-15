import telegram
from telegram.ext import ContextTypes

import core


async def income(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    sheet = core.get_sheet()

    try:
        if len(context.args) == 0:
            clean_income = sheet.get("I14", value_render_option="UNFORMATTED_VALUE")
            try:
                value = int(clean_income[0][0])
            except:
                value = 0

            await update.message.reply_text(f"Clean Income: Rp{value:,}")
            return

        value = int(context.args[0])
        sheet.update("I13", [[value]])
        await update.message.reply_text(f"Saved Income: Rp{value:,}")

    except:
        await update.message.reply_text(
            "Usage:\n"
            "/income amount\n"
            "/income"
        )
