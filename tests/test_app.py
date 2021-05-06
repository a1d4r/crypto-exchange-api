from flask import Flask
from sqlalchemy.orm import Session

from crypto_exchange.currencies.models import Currency
from crypto_exchange.migration import fill_database
from crypto_exchange.tasks import update_currencies
from crypto_exchange.users.models import User


def test_app_exists(app: Flask):
    assert app is not None


def test_app_is_testing(app: Flask):
    assert app.config['TESTING'] is True


def test_populate(session):
    fill_database()
    assert session.query(User).count() > 0
    assert session.query(Currency).count() >= 5


def test_app():
    from crypto_exchange.app import app

    assert app.config['TESTING'] is False


def test_task(session: Session, currency_factory):
    currency = currency_factory()
    rates = [currency.buying_rate, currency.selling_rate]
    update_currencies()
    session.refresh(currency)

    new_rates = [currency.buying_rate, currency.selling_rate]
    assert rates != new_rates
