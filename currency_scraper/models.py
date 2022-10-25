from pydantic import BaseModel


class Currency(BaseModel):
    currency_code: str
    currency_name: str
    convertion_rate: int
    currency_avg_rate: float
