from telegram import Update
from telegram.ext import ContextTypes

async def agent20(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tachyon 20 under Robdoe Agency.")
