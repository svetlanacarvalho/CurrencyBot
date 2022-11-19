import telebot
from config import *
from extensions import Converter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help (message: telebot.types.Message):
    text = 'Привет! Чтобы начать работу введи команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\n Просмотреть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        quote, base, amount = message.text.split()
    except ValueError as e:
        bot.reply_to(message, f'Слишком много параметров. Попробуй ещё раз.')
    else:
        try:
            text = Converter.get_price(quote, base, amount)
            bot.send_message(message.chat.id, text)
        except APIException as e:
            bot.reply_to(message, f'Ошибка в команде:\n{e}')


bot.polling()