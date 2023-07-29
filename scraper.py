from bs4 import BeautifulSoup
import requests

pult_url = 'https://www.pult.ru/'
citilink_url = 'https://www.citilink.ru/'
doctorhead_url = 'https://doctorhead.ru/'


def get_price(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    price = 0
    if url[:len(pult_url)] == pult_url:
        price = soup.find("div", class_="amount amount--lg amount--current")
        price = price.get_text().replace(" ", "").replace("\n", "")

    elif url[:len(citilink_url)] == citilink_url:
        price = soup.find("a", class_="app-catalog-9gnskf e1259i3g0")
        price = price.get_text().replace(" ", "").replace("\n", "")

    elif url[:len(doctorhead_url)] == doctorhead_url:
        price = soup.find("span", class_="nowrap")
        price = price.get_text().replace(" ", "").replace("\n", "")
    return ''.join(filter(str.isdigit, price))

# https://www.pult.ru/product/provodnye-naushniki-audio-technica-ath-m50x
# https://www.citilink.ru/product/naushniki-audio-technica-ath-m50x-3-5-mm-monitornye-chernyi-15117007-1048584/
