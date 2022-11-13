import os
from datetime import date, datetime

from pymongo import MongoClient

from currency_scraper.singleton import Singleton


class Database(metaclass=Singleton):
    def __init__(self) -> None:
        self.client = MongoClient(
            os.environ.get("MONGODB_URI"), serverSelectionTimeoutMS=5000
        )
        self.db = self.client['currencies_db']
        self.currency_collections = self.client['currencies_db']['currencies']

    @staticmethod
    def _get_date_filter(date: date):
        return {
            'date': {
                '$gte': date,
                '$lte': date,
            }
        }

    @staticmethod
    def _get_currency_filter(currency_code: str):
        return {'currency_code': currency_code.upper()}

    def get_all_currencies(self):
        result = self.currency_collections.find({}, {'_id': 0}).sort(
            'date', -1
        )
        return list(result)

    def get_currency_from_all_dates(self, currency_code: str) -> list:
        query = Database._get_currency_filter(currency_code)
        result = self.currency_collections.find(query, {'_id': 0}).sort(
            'date', -1
        )
        return list(result)

    def get_currency_from_provided_date(self, currency_code: str, date: date):
        date = datetime.combine(
            date, datetime.min.time()
        )  # convert date(pymongo does not support it) to datetime
        query = Database._get_date_filter(
            date
        ) | Database._get_currency_filter(currency_code)
        result = self.currency_collections.find_one(query, {'_id': 0})
        return result

    def is_date_in_database(self, date: datetime):
        query = Database._get_date_filter(date)
        if self.currency_collections.find_one(query):
            return True
        return False

    def insert_currencies(self, currencies: list[dict]):
        self.currency_collections.insert_many(currencies)
        return currencies
