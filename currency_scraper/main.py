from fastapi import FastAPI

from scraper import scrap_currencies_from_html

app = FastAPI()


@app.get("/currency/{currency_code}")
async def fetch_currency(currency_code):
    currencies = scrap_currencies_from_html()
    return currencies[currency_code.upper()]
