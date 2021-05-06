from typing import List

from flask import Blueprint, abort
from flask_pydantic import validate

from crypto_exchange.database import create_session

from .models import Currency
from .schemas import CurrencyRequestBody, CurrencyResponseBody

currencies = Blueprint('currencies', __name__)


@currencies.route('/<int:currency_id>/', methods=['GET'])
@validate()
def get_currency(currency_id: int) -> CurrencyResponseBody:
    with create_session() as session:
        currency = session.query(Currency).get(currency_id)
        if not currency:
            abort(404)
        return CurrencyResponseBody.from_orm(currency)


@currencies.route('/', methods=['POST'])
@validate()
def create_currency(body: CurrencyRequestBody) -> CurrencyResponseBody:
    with create_session() as session:
        currency = Currency(**body.dict())
        session.add(currency)
        session.flush()
        return CurrencyResponseBody.from_orm(currency)


@currencies.route('/', methods=['GET'])
@validate(response_many=True)
def list_currencies() -> List[CurrencyResponseBody]:
    with create_session() as session:
        currencies = session.query(Currency).all()
        return [CurrencyResponseBody.from_orm(currency) for currency in currencies]
