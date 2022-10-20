from __future__ import annotations

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

NAME, CODE, AVG_RATE = 0, 1, -1

# WORKING FINE
class Currency(BaseModel):
    currency_name: str
    convertion_rate: int
    currency_avg_rate: float

    # NOT WORKING
    # def get_currency_convertion_rate(self, other: Currency):
    #     return self.currency_avg_rate / other.currency_avg_rate


def scrap_currencies_from_xml():
    # PROBLEM with mutable url -> changes number after a and date after z each day
    url = 'https://www.nbp.pl/kursy/xml/a202z221018.xml'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    currency_xml_tags = soup('pozycja')  # shortcut for find_all()
    currencies: dict[str, Currency] = {}

    for currency in currency_xml_tags:
        currencies[currency.kod_waluty.string] = Currency(
            currency_name=currency.nazwa_waluty.string,
            convertion_rate=int(currency.przelicznik.string),
            currency_avg_rate=float(
                currency.kurs_sredni.string.replace(',', '.')
            ),
        )
    return currencies


def _get_page_soup(url: str) -> BeautifulSoup:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')
    return soup


def scrap_currencies_from_html() -> dict[str, Currency]:
    url = 'https://www.nbp.pl/Kursy/KursyA.html'
    soup = _get_page_soup(url)
    currencies: dict[str, Currency] = {}

    for tr_tag in soup.tbody.find_all('tr', recursive=False):
        # td.text[:-2] is there to get rid of '*)' sign in Ukrainian currency
        currency_data = [
            td.string if td.string is not None else td.text[:-2]
            for td in tr_tag.find_all('td')
        ]
        # -3 is currency code start index - never changes, the rest is convertion rate eg. 100 HUF
        currency_code = currency_data[CODE][-3:]
        convertion_rate = int(currency_data[CODE][:-3])

        currencies[currency_code] = Currency(
            currency_name=currency_data[NAME],
            convertion_rate=convertion_rate,
            currency_avg_rate=float(currency_data[AVG_RATE].replace(',', '.')),
        )

    return currencies
