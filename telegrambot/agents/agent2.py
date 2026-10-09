from telegram import Update
from telegram.ext import ContextTypes

async def agent2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tachyon 2 under Robdoe Agency.")
