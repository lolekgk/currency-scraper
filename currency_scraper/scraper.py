import re
from datetime import datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from currency_scraper.models import Currency


class NbpCurrencyScrapper:

    base_url = 'https://www.nbp.pl/'

    @staticmethod
    def _get_page(*, url: str, parser: str) -> BeautifulSoup:
        page = requests.get(url)
        return BeautifulSoup(page.content, parser)

    def _get_absolute_url_from_href(
        self, *, soup: BeautifulSoup, pattern: str
    ) -> str:
        relative_url = soup.find(href=re.compile(pattern)).get('href')
        return urljoin(self.base_url, relative_url)

    def _get_html_table_page(self) -> BeautifulSoup:
        main_page = self._get_page(url=self.base_url, parser='lxml')
        html_table_page_url = self._get_absolute_url_from_href(
            soup=main_page, pattern='tabela'
        )
        return self._get_page(url=html_table_page_url, parser='lxml')

    def _get_xml_table_page(self) -> BeautifulSoup:
        html_table_page = self._get_html_table_page()
        xml_table_page_url = self._get_absolute_url_from_href(
            soup=html_table_page, pattern='xml'
        )
        return self._get_page(url=xml_table_page_url, parser='xml')

    def scrap_publication_date(self) -> datetime:
        xml_table_page = self._get_xml_table_page()
        publication_date_str = xml_table_page.find('data_publikacji').string
        return datetime.strptime(publication_date_str, '%Y-%m-%d')

    def scrap_currencies_with_publication_date(self) -> list[dict]:
        xml_table_page = self._get_xml_table_page()
        publication_date = self.scrap_publication_date()
        currencies = []

        for currency in xml_table_page('pozycja'):
            currencies.append(
                Currency(
                    currency_code=currency.kod_waluty.string,
                    currency_name=currency.nazwa_waluty.string,
                    convertion_rate=int(currency.przelicznik.string),
                    currency_avg_rate=float(
                        currency.kurs_sredni.string.replace(',', '.')
                    ),
                    date=publication_date,
                ).dict()
            )
        return currencies
