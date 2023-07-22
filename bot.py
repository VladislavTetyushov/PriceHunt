import time
import telebot
from telebot import types
import scraper
from dotenv import load_dotenv
import os

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'));

need_check = True
price_from_pult = 0
price_from_citilink = 0
price_from_doctorhead = 0
url_list = []

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Ввести ссылки")
btn2 = types.KeyboardButton("stop PULT")
markup.add(btn1, btn2)


def check_price(user_id, url):
    global need_check
    global price_from_pult
    while need_check:
        new_price = scraper.get_price(url)
        if price_from_pult != new_price:
            price_from_pult = new_price
            bot.send_message(user_id, new_price)
        time.sleep(600)


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
    global need_check
    global url_list
    if message.text == "Ввести ссылки":
        bot.send_message(message.from_user.id, "Отправьте ссылки на магазины")

    elif message.text[:len(scraper.pult_url)] == scraper.pult_url or \
            message.text[:len(scraper.citilink_url)] == scraper.citilink_url or \
            message.text[:len(scraper.doctorhead_url)] == scraper.doctorhead_url:
        url_list.append(message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Нет")
        btn2 = types.KeyboardButton("Да")
        markup.add(btn1, btn2)

        bot.send_message(message.from_user.id, "Ссылка добавлена, добавить еще? 👀", reply_markup=markup)

    elif message.text == "Да":
        bot.send_message(message.from_user.id, "Жду ссылку :)")

    elif message.text == "Нет":
        need_check = True
        bot.send_message(message.from_user.id, "Начинаю отслеживание 👀")
        print(url_list)
        check_price(message.from_user.id, url_list[0])
        check_price(message.from_user.id, url_list[1])

    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Привет, введи ссылку на товар с сайта pult")

    elif message.text == "stop PULT":
        bot.send_message(message.from_user.id, "Отслеживание прекращено")
        need_check = False

    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


bot.polling(none_stop=True, interval=0)
