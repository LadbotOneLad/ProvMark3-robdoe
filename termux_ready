import telebot
import subprocess

# ----------------------------------------------------
#  BOT TOKEN (8895929865:AAFVSR-ECLVlo63tqTts_0ZbkABJAAzdIWs)
# ----------------------------------------------------
bot = telebot.TeleBot("8895929865:AAFVSR-ECLVlo63tqTts_0ZbkABJAAzdIWs")

# ----------------------------------------------------
#  /ping  → bot replies "PONG"
# ----------------------------------------------------
@bot.message_handler(commands=['ping'])
def ping(m):
    bot.reply_to(m, "PONG")

# ----------------------------------------------------
#  /node3  → runs your Termux script: node3.py
# ----------------------------------------------------
@bot.message_handler(commands=['node3'])
def node3(m):
    try:
        out = subprocess.check_output(["python", "node3.py"])
        bot.reply_to(m, out.decode())
    except Exception as e:
        bot.reply_to(m, f"Error: {e}")

# ----------------------------------------------------
#  /weather  → runs weather.py (your swarm script)
# ----------------------------------------------------
@bot.message_handler(commands=['weather'])
def weather(m):
    try:
        out = subprocess.check_output(["python", "weather.py"])
        bot.reply_to(m, out.decode())
    except Exception as e:
        bot.reply_to(m, f"Error: {e}")

# ----------------------------------------------------
#  Identity-trigger example
#  If message contains GENESIS → run genesis.py
# ----------------------------------------------------
@bot.message_handler(func=lambda msg: True)
def identity_trigger(m):
    text = m.text.upper()

    if "GENESIS" in text:
        try:
            out = subprocess.check_output(["python", "genesis.py"])
            bot.reply_to(m, out.decode())
        except Exception as e:
            bot.reply_to(m, f"Error: {e}")

    elif "ATOM" in text:
        bot.reply_to(m, "ATOM NODE ACKNOWLEDGED")

    elif "TRUTH" in text:
        bot.reply_to(m, "TRUTH VECTOR ONLINE")

# ----------------------------------------------------
#  Start bot
# ----------------------------------------------------
bot.polling()
