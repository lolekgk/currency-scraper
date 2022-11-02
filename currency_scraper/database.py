import os
from datetime import date, datetime, timedelta

from pymongo import MongoClient

from currency_scraper.scraper import NbpCurrencyScrapper
from currency_scraper.singleton import Singleton


class Database(metaclass=Singleton):
    def __init__(self) -> None:
        self.client = MongoClient(
            os.environ.get("MONGODB_URI"), serverSelectionTimeoutMS=5000
        )
        self.db = self.client['currencies_db']
        self.currency_collections = self.client['currencies_db']['currencies']

    def get_all_currencies(self):
        self.insert_currencies()
        result = self.currency_collections.find({}, {'_id': 0}).sort(
            'date', -1
        )
        return list(result)

    def get_currency_from_all_dates(self, currency_code: str) -> list:
        self.insert_currencies()
        query = {'currency_code': currency_code.upper()}
        result = self.currency_collections.find(query, {'_id': 0}).sort(
            'date', -1
        )
        return list(result)

    def insert_currencies(self):
        scraper = NbpCurrencyScrapper()
        date = scraper.scrap_publication_date()
        query = {
            'date': {
                '$gte': date,
                '$lt': date + timedelta(seconds=1),
            }
        }
        if not self.currency_collections.find_one(query):
            currencies = scraper.scrap_currencies_with_publication_date()
            self.currency_collections.insert_many(currencies)

    def get_currency_from_provided_date(self, currency_code: str, date: date):
        date = datetime.combine(date, datetime.min.time())
        query = {
            'date': {
                '$gte': date,
                '$lt': date + timedelta(seconds=1),
            },
            'currency_code': currency_code.upper(),
        }
        result = self.currency_collections.find_one(query, {'_id': 0})
        return result
