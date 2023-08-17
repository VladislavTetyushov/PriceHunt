from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

stores_urls = {
    "pult": "https://www.pult.ru/",
    "doctorhead": "https://doctorhead.ru/",
    "citilink": "https://www.citilink.ru/",
}


class PriceParser(ABC):
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    def get_price(self) -> str:
        pass


class PultParser(PriceParser):
    def get_price(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "html.parser")
        price = soup.find("div", class_="amount amount--lg amount--current")
        if price is not None:
            price = price.get_text().replace(" ", "").replace("\n", "")
            return "".join(filter(str.isdigit, price))
        return None


class DoctorheadParser(PriceParser):
    def get_price(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "html.parser")
        price = soup.find("span", class_="nowrap")
        if price is not None:
            price = price.get_text().replace(" ", "").replace("\n", "")
            return "".join(filter(str.isdigit, price))
        return None


class CitilinkParser(PriceParser):
    def get_price(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.text, "html.parser")
        price = soup.find("a", class_="app-catalog-9gnskf e1259i3g0")
        if price is not None:
            price = price.get_text().replace(" ", "").replace("\n", "")
            return "".join(filter(str.isdigit, price))
        return None


def price_parser_factory(url: str):
    # url_map = {
    #     stores_urls["pult"] : PultParser,
    #     stores_urls["doctorhead"] : DoctorheadParser,
    #     stores_urls["citilink"] : CitilinkParser
    # }

    if url[: len(stores_urls["pult"])] == stores_urls["pult"]:
        return PultParser(url)
    elif url[: len(stores_urls["doctorhead"])] == stores_urls["doctorhead"]:
        return DoctorheadParser(url)
    elif url[: len(stores_urls["citilink"])] == stores_urls["citilink"]:
        return CitilinkParser(url)
    else:
        return None


def get_price(url: str):
    result = price_parser_factory(url)
    if result is not None:
        return result.get_price()
    return None


# def price_parser(url: str, tag: str, class_name: str):
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, "html.parser")
#     price = soup.find(tag, class_=class_name)
#     if price != None:
#         price = price.get_text().replace(" ", "").replace("\n", "")
#         return "".join(filter(str.isdigit, price))
#     return None


# https://www.pult.ru/product/provodnye-naushniki-audio-technica-ath-m50x
# https://www.citilink.ru/product/naushniki-audio-technica-ath-m50x-3-5-mm-monitornye-chernyi-15117007-1048584/
