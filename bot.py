import os
import time
from urllib.parse import urlparse

import telebot
from dotenv import load_dotenv
from telebot import types

import scraper

load_dotenv()
TOKEN = os.getenv("TOKEN")
assert TOKEN is not None
bot = telebot.TeleBot(TOKEN)

need_check = True
price_from_pult = 0
price_from_citilink = 0
price_from_doctorhead = 0
url_dict = {}
interval = 600

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Ввести ссылки")
btn2 = types.KeyboardButton("Прекратить отслеживание")
markup.add(btn1, btn2)


def get_company_name(url):
    parsed_url = urlparse(url)
    company_name = parsed_url.netloc.split(".")
    if len(company_name) == 3:
        return company_name[1]
    return company_name[0]


def check_price(user_id, urls):
    global need_check
    price = 0
    while need_check:
        bot.send_message(user_id, "Я весь в работе")
        for url in urls.items():
            print(url)
            new_price = scraper.get_price(url[1])
            if price != new_price:
                price = new_price
                bot.send_message(user_id, url[0] + ": " + price + "р")
        time.sleep(600)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        text="Привет, {0.first_name}!".format(message.from_user),
        reply_markup=markup,
    )
    # SQLdata.execute_query(f"INSERT INTO users (user_id) VALUES ({message.chat.id})")


@bot.message_handler(commands=["stop"])
def stop(message):
    bot.send_message(message.chat.id, "Бот остановлен")


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    global need_check
    global url_dict
    price = scraper.get_price(message.text)

    if price is not None:
        url_dict[get_company_name(message.text)] = message.text
        bot.send_message(message.from_user.id, "Ссылка добавлена")

    elif message.text == "Начать отслеживание":
        need_check = True
        if len(url_dict) == 0:
            bot.send_message(
                message.from_user.id, "Вы еще не добавили ссылок для отслеживания :)"
            )
        else:
            check_price(message.chat.id, url_dict)
            bot.send_message(message.from_user.id, "Отслеживание началось")

    elif message.text == "Прекратить отслеживание":
        bot.send_message(message.from_user.id, "Отслеживание прекращено")
        need_check = False
        url_dict = {}
    elif price is None:
        bot.send_message(
            message.from_user.id,
            "Данная ссылка или текст не подходят для отслеживания, введите ссылку на товар из магазина Pult, Doctorhead, Citilink",
        )


bot.polling(none_stop=True, interval=0)
