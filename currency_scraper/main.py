from datetime import date

from fastapi import FastAPI, HTTPException, status

from currency_scraper.database import Database

app = FastAPI()


@app.get("/currencies", tags=['currencies'])
def get_all_currencies():
    return Database().get_all_currencies()


@app.get("/currencies/{currency_code}", tags=['currencies'])
def get_currency_from_specific_date(
    currency_code: str, date: date | None = None
):
    currency = Database().get_currency_from_all_dates(currency_code)
    if date:
        currency = Database().get_currency_from_provided_date(
            currency_code, date
        )

    if not currency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Currency not found.",
        )
    return currency
