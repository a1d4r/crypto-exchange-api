from flask import Response
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from crypto_exchange.users.models import User
from crypto_exchange.users.schemas import (
    UserCurrencyListResponseBody,
    UserCurrencyResponseBody,
    UserListResponseBody,
    UserResponseBody,
)


def test_get_user(client: FlaskClient, user_factory):  # type: ignore
    user = user_factory(balance=1337)
    response: Response = client.get('/users/1/')
    assert response.status_code == 200

    actual_user = UserResponseBody.from_orm(user)
    retrieved_user = UserResponseBody.parse_raw(response.data)
    assert actual_user == retrieved_user


def test_post_user(client: FlaskClient, session: Session):  # type: ignore
    response: Response = client.post('/users/')
    assert response.status_code == 200

    user = session.query(User).get(1)
    actual_user = UserResponseBody.from_orm(user)
    retrieved_user = UserResponseBody.parse_raw(response.data)
    assert actual_user == retrieved_user


def test_list_users(client: FlaskClient, user_factory):  # type: ignore
    users = user_factory.create_batch(3)
    response: Response = client.get('/users/')
    assert response.status_code == 200

    actual_users = UserListResponseBody(__root__=users)
    retrieved_users = UserListResponseBody.parse_raw(response.data)
    assert actual_users == retrieved_users


def test_get_user_currencies(client: FlaskClient, user_currency_factory):  # type: ignore
    uc = user_currency_factory()
    response: Response = client.get('/users/1/currencies/1/')
    assert response.status_code == 200

    actual_uc = UserCurrencyResponseBody.from_orm(uc)
    retrieved_uc = UserCurrencyResponseBody.parse_raw(response.data)
    assert actual_uc == retrieved_uc


def test_list_user_currencies(
    client: FlaskClient, user_factory, user_currency_factory  # type: ignore
):
    user = user_factory()
    ucs = user_currency_factory.create_batch(3, user=user)
    response: Response = client.get('/users/1/currencies/')
    assert response.status_code == 200

    actual_currencies = UserCurrencyListResponseBody(__root__=ucs)
    retrieved_currencies = UserCurrencyListResponseBody.parse_raw(response.data)
    assert actual_currencies == retrieved_currencies
