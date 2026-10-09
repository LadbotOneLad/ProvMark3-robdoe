from telegram import Update
from telegram.ext import ContextTypes

async def agent4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tachyon 4 under Robdoe Agency.")
