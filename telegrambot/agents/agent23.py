from telegram import Update
from telegram.ext import ContextTypes

async def agent23(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tachyon 23 under Robdoe Agency.")
