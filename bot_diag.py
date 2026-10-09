import telebot

print(">>> BOT DIAGNOSTIC STARTING")

try:
    bot = telebot.TeleBot("8895929865:AAFVSR-ECLVlo63tqTts_0ZbkABJAAzdIWs")
    print(">>> TOKEN LOADED")
except Exception as e:
    print(">>> TOKEN ERROR:", e)

@bot.message_handler(commands=['ping'])
def ping(m):
    print(">>> RECEIVED /ping")
    bot.reply_to(m, "PONG")

print(">>> STARTING POLLING...")
bot.polling(none_stop=True, interval=0)
