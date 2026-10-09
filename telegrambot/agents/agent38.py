from telegram import Update
from telegram.ext import ContextTypes

async def agent38(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tachyon 38 under Robdoe Agency.")
