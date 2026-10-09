import telebot
import subprocess

bot = telebot.TeleBot("8895929865:AAFVSR-ECLVlo63tqTts_0ZbkABJAAzdIWs")

# ----------------------------------------------------
#  /esp  → checks ESP32 connection
# ----------------------------------------------------
@bot.message_handler(commands=['esp'])
def esp(m):
    try:
        out = subprocess.check_output(["python", "esp32_check.py"])
        bot.reply_to(m, out.decode())
    except Exception as e:
        bot.reply_to(m, f"ESP32 ERROR: {e}")

bot.polling()
