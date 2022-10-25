import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from models import Currency

BASE_URL = 'https://www.nbp.pl/'


def _get_page_soup(*, url: str, parser: str) -> BeautifulSoup:
    page = requests.get(url)
    return BeautifulSoup(page.content, parser)


def _get_absolute_url_from_href(*, soup: BeautifulSoup, pattern: str) -> str:
    relative_url = soup.find(href=re.compile(pattern)).get('href')
    return urljoin(BASE_URL, relative_url)


def _get_html_table_page_soup() -> BeautifulSoup:
    main_page_soup = _get_page_soup(url=BASE_URL, parser='lxml')
    html_table_url = _get_absolute_url_from_href(
        soup=main_page_soup, pattern='tabela'
    )
    return _get_page_soup(url=html_table_url, parser='lxml')


def _get_xml_table_page_soup() -> BeautifulSoup:
    html_table_soup = _get_html_table_page_soup()
    xml_table_url = _get_absolute_url_from_href(
        soup=html_table_soup, pattern='xml'
    )
    return _get_page_soup(url=xml_table_url, parser='xml')


def scrap_currencies() -> list[dict]:
    xml_table_page_soup = _get_xml_table_page_soup()
    currencies: list[dict] = []

    for currency in xml_table_page_soup('pozycja'):
        currencies.append(
            Currency(
                currency_code=currency.kod_waluty.string,
                currency_name=currency.nazwa_waluty.string,
                convertion_rate=int(currency.przelicznik.string),
                currency_avg_rate=float(
                    currency.kurs_sredni.string.replace(',', '.')
                ),
            ).dict()
        )
    return currencies
