from decimal import Decimal
from typing import List

from pydantic import BaseModel


class UserResponseBody(BaseModel):
    id: int
    balance: Decimal

    class Config:
        orm_mode = True


class UserCurrencyResponseBody(BaseModel):
    currency_id: int
    amount: Decimal = Decimal('0.00')

    class Config:
        orm_mode = True


class UserListResponseBody(BaseModel):
    __root__: List[UserResponseBody]

    class Config:
        orm_mode = True


class UserCurrencyListResponseBody(BaseModel):
    __root__: List[UserCurrencyResponseBody]

    class Config:
        orm_mode = True
