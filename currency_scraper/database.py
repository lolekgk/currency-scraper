import os

from dotenv import find_dotenv, load_dotenv
from pymongo import MongoClient

from currency_scraper.scraper import scrap_currencies
from currency_scraper.singleton import Singleton

load_dotenv(find_dotenv())

# username = os.environ.get("MONGODB_USERNAME")
# password = os.environ.get("MONGODB_PASSWORD")
# uri = os.environ.get("MONGODB_URI")


class Database(metaclass=Singleton):
    def __init__(self) -> None:
        self.client = MongoClient(
            os.environ.get("MONGODB_URI"), serverSelectionTimeoutMS=5000
        )
        self.db = self.client['currencies_db']
        self.currency_collections = self.db['currencies']

    def get_all_currencies(self):
        self.insert_currencies()
        result = self.currency_collections.find({}, {'_id': 0})
        return list(result)

    def insert_currencies(self):
        self.currency_collections.insert_many(scrap_currencies())


# client = MongoClient(
#     f"mongodb://{username}:{password}@localhost:27017/",
#     serverSelectionTimeoutMS=2000,
# )
# client = MongoClient("mongodb://{user}:{password}@{host}:{port}")


# currency_collections = db.currencies

# currencies = scrap_currencies()
# print(currencies)
# x = currency_collections.insert_many(currencies)


# print(x.inserted_ids)

# for x in currency_collections.find():
#     print(x)
