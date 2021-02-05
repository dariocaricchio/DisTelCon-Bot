import os
import telebot
from telebot import types
from dotenv import load_dotenv
load_dotenv()

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'), parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda m: m.text.isupper())
# @bot.message_handler(commands=['inline', 'letter'])
def inline_letter(message):
	markup = types.ReplyKeyboardMarkup()
	itembtna = types.KeyboardButton('a')
	itembtnv = types.KeyboardButton('v')
	itembtnc = types.KeyboardButton('c')
	itembtnd = types.KeyboardButton('d')
	itembtne = types.KeyboardButton('e')
	markup.row(itembtna, itembtnv)
	markup.row(itembtnc, itembtnd, itembtne)
	bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)


bot.polling()