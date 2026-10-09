from telegram import Update
from telegram.ext import ContextTypes

async def agent10(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tachyon 10 under Robdoe Agency.")
