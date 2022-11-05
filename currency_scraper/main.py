from datetime import date

from fastapi import FastAPI, HTTPException, status

from currency_scraper.database import Database
from currency_scraper.models import UserFriendlyCurrency
from currency_scraper.scraper import NbpCurrencyScrapper

app = FastAPI()


@app.get(
    "/currencies",
    tags=['currencies'],
    response_model=list[UserFriendlyCurrency],
)
def get_all_currencies():
    currencies = Database().get_all_currencies()
    if not currencies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Database is empty, please add some data.",
        )
    return currencies


@app.get(
    "/currencies/{currency_code}",
    tags=['currencies'],
    response_model=UserFriendlyCurrency | list[UserFriendlyCurrency],
)
def get_currency(currency_code: str, date: date | None = None):
    currency = (
        Database().get_currency_from_provided_date(currency_code, date)
        if date
        else Database().get_currency_from_all_dates(currency_code)
    )

    if not currency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Currency not found in database.",
        )
    return currency


@app.post(
    "/currencies",
    status_code=status.HTTP_201_CREATED,
    tags=['currencies'],
    response_model=list[UserFriendlyCurrency],
)
def add_currencies():
    scraper = NbpCurrencyScrapper()
    date = scraper.scrap_publication_date()
    if not Database().is_date_in_database(date):
        currencies = scraper.scrap_currencies(date)
        return Database().insert_currencies(currencies)
    raise HTTPException(
        status_code=409,
        detail=f"Currencies publicated on: '{date.date()}' already exists in database.",
    )
