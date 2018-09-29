import re

import cherrypy
import telebot

import config
from scrapper import scrapper



bot = telebot.TeleBot(config.TOKEN)


class WebhookServer(object):
    _hi = None


@bot.message_handler(content_types=['text'])
def show_today(message):
    group = message.text.upper()
    print(group)
    if re.search(r'[0-9][А-Яа-я][0-9]([0-9]|[А-Яа-я])', group):
        weeks = scrapper.scrape_rasp(group=group)
        current_week = scrapper.get_current_week(both_weeks=weeks)
        text = scrapper.get_current_day(week=current_week)
    elif re.search(r'[Э][Т][О]([0-9]){2,3}', group):
        weeks = scrapper.scrape_rasp(group=group)
        current_week = scrapper.get_current_week(both_weeks=weeks)
        text = scrapper.get_current_day(week=current_week)
    else:
        text = 'Введите номер своей группы!'
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling(none_stop=True)
