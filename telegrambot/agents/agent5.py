from telegram import Update
from telegram.ext import ContextTypes

async def agent5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tachyon 5 under Robdoe Agency.")
