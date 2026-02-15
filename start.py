from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Welcome to Daily Expense Bot! Type /help to see available commands."
    await update.message.reply_text(text)
