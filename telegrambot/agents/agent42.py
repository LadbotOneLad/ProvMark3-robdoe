from telegram import Update
from telegram.ext import ContextTypes

async def agent42(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tachyon 42 under Robdoe Agency.")
