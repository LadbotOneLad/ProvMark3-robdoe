from telegram import Update
from telegram.ext import ContextTypes

async def agent51(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Tachyon 51 under Robdoe Agency.")
