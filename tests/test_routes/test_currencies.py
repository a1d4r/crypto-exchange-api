from flask import Response
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from crypto_exchange.currencies.models import Currency
from crypto_exchange.currencies.schemas import (
    CurrencyListResponseBody,
    CurrencyRequestBody,
    CurrencyResponseBody,
)


def test_get_currency(client: FlaskClient, currency_factory):  # type: ignore
    currency = currency_factory()
    response: Response = client.get('/currencies/1/')
    assert response.status_code == 200

    actual_currency = CurrencyResponseBody.from_orm(currency)
    retrieved_currency = CurrencyResponseBody.parse_raw(response.data)
    assert actual_currency == retrieved_currency


def test_post_currency(client: FlaskClient, session: Session, currency_factory):  # type: ignore
    payload = CurrencyRequestBody.from_orm(currency_factory.build()).json()
    response: Response = client.post('/currencies/', data=payload.encode())
    assert response.status_code == 200

    currency = session.query(Currency).get(1)
    actual_currency = CurrencyResponseBody.from_orm(currency)
    retrieved_currency = CurrencyResponseBody.parse_raw(response.data)
    assert actual_currency == retrieved_currency


def test_list_currencies(client: FlaskClient, session: Session, currency_factory):  # type: ignore
    currencies = currency_factory.create_batch(3)
    response: Response = client.get('/currencies/')
    assert response.status_code == 200

    actual_currencies = CurrencyListResponseBody(__root__=currencies)
    retrieved_currencies = CurrencyListResponseBody.parse_raw(response.data)
    assert actual_currencies == retrieved_currencies
