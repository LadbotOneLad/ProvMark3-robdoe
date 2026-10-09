from telegram import Update
from telegram.ext import ContextTypes

async def agent18(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tachyon 18 under Robdoe Agency.")
