from telegram import Update
from telegram.ext import ContextTypes

async def agent21(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tachyon 21 under Robdoe Agency.")
