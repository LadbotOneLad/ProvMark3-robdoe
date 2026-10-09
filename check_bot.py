import telebot

bot = telebot.TeleBot("8895929865:AAFVSR-ECLVlo63tqTts_0ZbkABJAAzdIWs")

@bot.message_handler(commands=['ping'])
def ping(m):
    bot.reply_to(m, "PONG")

bot.polling()
