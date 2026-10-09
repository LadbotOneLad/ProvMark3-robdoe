from telegram import Update
from telegram.ext import ContextTypes

async def agent6(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tachyon 6 under Robdoe Agency.")
