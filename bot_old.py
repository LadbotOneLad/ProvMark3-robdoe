import asyncio
from telebot.async_telebot import AsyncTeleBot
from witness import write_event

# ================================
# INSERT YOUR REAL TOKEN *LOCALLY*
# DO NOT SHARE IT ANYWHERE
# ================================
TOKEN = 8895929865:AAFVSR-ECLVlo63tqTts_0ZbkABJAAzdIWs

bot = AsyncTeleBot(TOKEN)

def header():
    return "⟡ ROBDOE UNIFIED WITNESS STREAM ⟡\n"

@bot.message_handler(commands=['start'])
async def start(message):
    write_event("TG", "START", f"chat_id={message.chat.id}")
    await bot.reply_to(
        message,
        header() +
        "Witness stream online.\n"
        "Ant‑Man micro‑events active.\n"
        "Everything you drop becomes part of the record."
    )

@bot.message_handler(commands=['tag'])
async def tag(message):
    parts = message.text.split(maxsplit=1)
    label = parts[1].strip() if len(parts) > 1 else "untagged"
    write_event("TG", "TAG", f"{message.chat.id}: {label}")
    await bot.reply_to(
        message,
        header() +
        f"Tagged this moment as: {label}"
    )

@bot.message_handler(commands=['log'])
async def log_cmd(message):
    from witness import LEDGER
    try:
        with open(LEDGER, "r") as f:
            data = f.readlines()
    except FileNotFoundError:
        await bot.reply_to(message, header() + "No witness entries yet.")
        return

    last = "".join(data[-60:])
    await bot.reply_to(
        message,
        header() +
        "Last 60 micro‑events:\n\n" +
        (last or "Empty.")
    )

@bot.message_handler(func=lambda m: True)
async def main(message):
    incoming = (message.text or "").strip()
    if not incoming:
        return

    write_event("TG", "MSG", f"{message.chat.id}: {incoming}")

    await bot.reply_to(
        message,
        header() +
        f"Recorded micro‑event:\n“{incoming}”\n"
        "Witness updated."
    )

async def main_loop():
    print("[ROBDOE] Unified Ant‑Man Witness Bot Booting…")
    await bot.infinity_polling()

if __name__ == "__main__":
    asyncio.run(main_loop())
