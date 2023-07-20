import time
import telebot
from telebot import types
import scraper
from dotenv import load_dotenv
import os

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'));
pult_url = 'https://www.pult.ru/'
need_check_pult = True
price_from_pult = 0

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("магазин PULT")
btn2 = types.KeyboardButton("stop PULT")
markup.add(btn1, btn2)


def check_price_pult(user_id, url):
    global need_check_pult
    global price_from_pult
    while need_check_pult:
        new_price = scraper.get_price_from_pult(url)
        if price_from_pult != new_price:
            price_from_pult = new_price
            bot.send_message(user_id, scraper.get_price_from_pult(url))
            time.sleep(3600)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}!".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(message.chat.id, 'Бот остановлен')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global need_check_pult
    if message.text == "магазин PULT":
        bot.send_message(message.from_user.id, "Введи ссылку на PULT")

    elif message.text[:len(pult_url)] == pult_url:
        bot.send_message(message.from_user.id, "Ссылка добавлена, начинаю отслеживание 👀")
        need_check_pult = True
        check_price_pult(message.from_user.id, message.text)

    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Привет, введи ссылку на товар с сайта pult")

    elif message.text == "stop PULT":
        bot.send_message(message.from_user.id, "Отслеживание прекращено")
        need_check_pult = False

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
