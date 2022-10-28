from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Currency(BaseModel):
    # id: UUID = Field(default_factory=uuid4, alias='_id')
    currency_code: str
    currency_name: str
    convertion_rate: int
    currency_avg_rate: float


# dodac _id
