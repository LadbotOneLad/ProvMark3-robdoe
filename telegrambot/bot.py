#!/usr/bin/env python3
import os
import importlib
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

def load_tachyons():
    handlers = {}
    for i in range(1, 52 + 1):
        module = importlib.import_module(f"agents.agent{i}")
        handler_func = getattr(module, f"agent{i}")
        handlers[f"agent{i}"] = handler_func
    return handlers

tachyons = load_tachyons()

async def start(update, context):
    await update.message.reply_text("Robdoe Tachyon Agency Online.")

async def ping(update, context):
    await update.message.reply_text("pong")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ping", ping))

for name, func in tachyons.items():
    app.add_handler(CommandHandler(name, func))

app.run_polling()
