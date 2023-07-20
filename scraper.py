from bs4 import BeautifulSoup
import requests


def get_price_from_pult(pult_url):
    r = requests.get(pult_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    price = soup.find("div", class_="amount amount--lg amount--current")
    price = price.get_text().replace(" ", "").replace("\n", "")
    return ''.join(filter(str.isdigit, price))

# https://www.pult.ru/product/provodnye-naushniki-audio-technica-ath-m50x
