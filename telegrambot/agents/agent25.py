from telegram import Update
from telegram.ext import ContextTypes

async def agent25(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tachyon 25 under Robdoe Agency.")
