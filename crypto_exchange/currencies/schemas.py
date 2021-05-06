from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel


class CurrencyRequestBody(BaseModel):
    name: str
    selling_rate: Decimal
    buying_rate: Decimal

    class Config:
        orm_mode = True


class CurrencyResponseBody(CurrencyRequestBody):
    id: int
    updated_at: datetime

    class Config:
        orm_mode = True


class CurrencyListResponseBody(BaseModel):
    __root__: List[CurrencyResponseBody]

    class Config:
        orm_mode = True
