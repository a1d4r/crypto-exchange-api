import pytest

from crypto_exchange.app import create_app
from crypto_exchange.database import create_session
from tests.factories import (
    CurrencyFactory,
    TransactionFactory,
    UserCurrencyFactory,
    UserFactory,
)


@pytest.fixture()
def app():
    app_ = create_app('testing')
    with app_.app_context():
        yield app_


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        client.environ_base['CONTENT_TYPE'] = 'application/json'
        yield client


@pytest.fixture()
def session(app):
    with create_session() as session:
        yield session


@pytest.fixture()
def user_factory(session):
    yield UserFactory(session)


@pytest.fixture()
def currency_factory(session):
    yield CurrencyFactory(session)


@pytest.fixture()
def user_currency_factory(session):
    yield UserCurrencyFactory(session)


@pytest.fixture()
def transaction_factory(session):
    yield TransactionFactory(session)
