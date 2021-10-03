import telebot
from config import keys, TOKEN
from extensions import ConvertionExeption, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def echo_test(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n ' \
           '<имя валюты цену которой хотите узнать> <имя валюты в которой надо узнать цену первой валюты> ' \
           '<количество первой валюты>\n ' \
           'Увидеть список возможных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        currency_values = message.text.split(' ')

        if len(currency_values) != 3:
            raise ConvertionExeption('Слишком много параметров')

        base, quote, amount = currency_values
        total_base = CurrencyConverter.get_price(base, quote, amount)*int(amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
