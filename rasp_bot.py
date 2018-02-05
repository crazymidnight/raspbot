import re

from flask import Flask, request
import telebot

import config
from scrapper import scrapper

server = Flask(__name__)
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=['text'])
def show_today(message):
    group = message.text
    text = scrapper.scrape_today(group=group)
    if re.search(r'[0-9][А-Яа-я][0-9][0-9]', group):
        text = scrapper.scrape_today(group=group)
    else:
        text = 'Введите номер своей группы!'
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling(none_stop=True)





