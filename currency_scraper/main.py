from fastapi import FastAPI

from currency_scraper.scraper import scrap_currencies_from_html

app = FastAPI()


@app.get("/currencies")
def fetch_all_currencies():
    currencies = scrap_currencies_from_html()
    return currencies


@app.get("/currencies/{currency_code}")
def fetch_currency(currency_code):
    currencies = scrap_currencies_from_html()
    return currencies.get(currency_code.upper())
