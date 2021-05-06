from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel

from .models import TransactionType


class TransactionBody(BaseModel):
    user_id: int
    currency_id: int
    type: TransactionType
    amount: Decimal


class TransactionListQuery(BaseModel):
    last_id: int = 0


class CreateTransactionBody(TransactionBody):
    currency_updated_at: datetime

    class Config:
        orm_mode = True


class TransactionResponseBody(TransactionBody):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TransactionListResponseBody(BaseModel):
    __root__: List[TransactionResponseBody]

    class Config:
        orm_mode = True
