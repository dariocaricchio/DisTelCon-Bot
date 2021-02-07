import os
import telebot
from poll import *
from telebot import types
from dotenv import load_dotenv
load_dotenv()
import re
import const
from replit import db

bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'), parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

polls = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?\nUse /help to see what commands you can use!😉")

# @bot.message_handler(func=lambda m: m.text.isupper())
@bot.message_handler(commands=['help'])
def inline_letter(message):
	markup = types.ReplyKeyboardMarkup()
	itembtn_newpoll = types.KeyboardButton('/new_poll')
	itembtn_polllist = types.KeyboardButton('/poll_list')
	# itembtnv = types.KeyboardButton('v')
	# itembtnc = types.KeyboardButton('c')
	# itembtnd = types.KeyboardButton('d')
	# itembtne = types.KeyboardButton('e')
	# markup.row(itembtna, itembtnv)
	# markup.row(itembtnc, itembtnd, itembtne)
	markup.row(itembtn_newpoll, itembtn_polllist)
	bot.send_message(message.chat.id, "You know, you can use one of the following commands:", reply_markup=markup)

@bot.message_handler(commands=['new_poll'])
def new_poll(message):
	msg = bot.reply_to(message,"A new poll, ah?🤔 So, what's the question?")
	bot.register_next_step_handler(msg, process_poll_name_step)

def process_poll_name_step(message):
	try:
		chat_id = message.chat.id
		question = message.text
		poll = Poll(id = chat_id, question = question)
		polls[chat_id] = poll
		msg = bot.reply_to(message, 'Cool!😁 And what are the answers? Put each answer on a different line please 🤗')
		bot.register_next_step_handler(msg, process_answers_step)
	except Exception as e:
		print(e)
		bot.reply_to(message, const.ERROR_MSG)

def split_on_empty_lines(s):
    # greedily match 1 or more new-lines
    blank_line_regex = r"(?:\r?\n){1,}"
    return re.split(blank_line_regex, s.strip())

def process_answers_step(message):
	try:
		chat_id = message.chat.id
		answers = split_on_empty_lines(message.text)
		if answers == [] or len(answers) == 0:
			msg = bot.reply_to(message, 'A poll without answers? Really? 😅 Put each answer on a different line please 🤗')
			bot.register_next_step_handler(msg, process_age_step)
			return
		poll = polls[chat_id]
		poll.answers = answers
		bot.send_message(chat_id, f'Nice! Your new poll is ready and its ID is {chat_id} 😎')
	except Exception as e:
		print(e)
		bot.reply_to(message, const.ERROR_MSG)

@bot.message_handler(commands=['poll_list'])
def poll_list(message):
	try:
		if len(polls) == 0:
			bot.reply_to(message, "Seems like there is no poll here!😁")
			return
		markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
		for k in polls.keys():
			markup.add(str(k))
		msg = bot.reply_to(message, 'What poll do you want to see?', reply_markup=markup)
		bot.register_next_step_handler(msg, show_poll)
	except Exception as e:
		print(e)
		bot.reply_to(message, const.ERROR_MSG)

def show_poll(message):
	try:
		poll_id = int(message.text) if message.text.isdigit() else None
		if poll_id == None or poll_id not in polls.keys():
			bot.reply_to(message,"Unknown poll id 🙅‍♂️")
		else:
			poll = polls[poll_id]
			bot.reply_to(message, f"Here it is:\n\n{poll}")
	except Exception as e:
		print(e)
		bot.reply_to(message, const.ERROR_MSG)


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
# 	bot.reply_to(message, message.text)

'''
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
                               InlineKeyboardButton("No", callback_data="cb_no"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Answer is No")

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup
'''

def main():
	print("TelBot is on its way!")
	bot.polling()
