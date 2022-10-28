import os

from fastapi import FastAPI

from currency_scraper.database import Database
from currency_scraper.scraper import scrap_currencies

app = FastAPI()


@app.get("/currencies")
def get_all_currencies():
    currencies = scrap_currencies()
    return currencies


@app.get("/test")
def get_all_currencies1():
    db = Database()
    return db.get_all_currencies()


# @app.get("/currencies/{currency_code}")
# def get_currency(currency_code: str):
#     currencies = scrap_currencies()
#     return currencies.get(currency_code.upper())
