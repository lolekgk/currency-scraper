import datetime

from pydantic import BaseModel


class Currency(BaseModel):
    currency_code: str
    currency_name: str
    convertion_rate: int
    currency_avg_rate: float
    date: datetime.datetime


class UserFriendlyCurrency(Currency):
    date: datetime.date  # date instead of datetime with a lot of 0
