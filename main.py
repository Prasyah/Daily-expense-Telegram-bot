from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

import core
import start as start_mod
from Feature import income as income_mod
from Feature import exp as exp_mod
from Feature import reimburse as reimburse_mod
from Feature import delete as delete_mod
from Feature import edit as edit_mod
from Feature import budget as budget_mod
from Feature import detail as detail_mod
from Feature import month as month_mod
from Feature import help as help_mod


def main():
    app = ApplicationBuilder().token(core.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_mod.start))
    app.add_handler(CommandHandler("income", income_mod.income))
    app.add_handler(CommandHandler("exp", exp_mod.exp))
    app.add_handler(CommandHandler("reimburse", reimburse_mod.reimburse))
    app.add_handler(CommandHandler("delete", delete_mod.delete))
    app.add_handler(CommandHandler("edit", edit_mod.edit))
    app.add_handler(CommandHandler("budget", budget_mod.budget))
    app.add_handler(CallbackQueryHandler(budget_mod.budget_callback, pattern="^budget_"))
    app.add_handler(CommandHandler("detail", detail_mod.detail))
    app.add_handler(CommandHandler("month", month_mod.month))
    app.add_handler(CallbackQueryHandler(month_mod.month_callback, pattern="^month_"))
    app.add_handler(CommandHandler("help", help_mod.help))

    print("Bot running")
    app.run_polling()


if __name__ == "__main__":
    main()
