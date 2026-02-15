import telegram
from telegram.ext import ContextTypes
import calendar
from datetime import datetime

import core


async def budget(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    sheet = core.get_sheet()

    categories = sheet.get("H2:H10")
    leftover = sheet.get("K2:K10", value_render_option="UNFORMATTED_VALUE")

    now = datetime.now()
    today = now.day
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    days_left = days_in_month - today
    if days_left == 0:
        days_left = 1

    text = "📊 Budget Left This Month\n\n"

    for i in range(len(categories)):
        cat = categories[i][0]
        try:
            left = int(float(leftover[i][0]))
        except:
            left = 0

        if cat == "Lunch":
            per_day = left // days_left
            text += (
                f"{cat}\n"
                f"Left: Rp{left:,}\n"
                f"Per day: Rp{per_day:,}\n\n"
            )
        else:
            text += (
                f"{cat}\n"
                f"Left: Rp{left:,}\n\n"
            )

    await update.message.reply_text(text)
