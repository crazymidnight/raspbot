import telebot

import config
from scrapper import scrapper

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(content_types=['text'])
def show_today(message):
    group = message.text
    text = scrapper.scrape_today(group=group)
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    bot.polling(none_stop=True)





