import json
from typing import List

from flask import Blueprint, abort, current_app
from flask_pydantic import validate
from werkzeug import Response
from werkzeug.exceptions import HTTPException

from crypto_exchange.currencies.models import Currency
from crypto_exchange.database import create_session
from crypto_exchange.transactions.models import Transaction
from crypto_exchange.transactions.schemas import (
    TransactionListQuery,
    TransactionResponseBody,
)

from .models import User, UserCurrency
from .schemas import UserCurrencyResponseBody, UserResponseBody

users = Blueprint('users', __name__)


@users.app_errorhandler(HTTPException)
def handle_exception(e: HTTPException) -> Response:
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {
            'code': e.code,
            'name': e.name,
            'description': e.description,
        }
    )
    response.content_type = 'application/json'
    return response


@users.route('/<int:user_id>/', methods=['GET'])
@validate()
def get_user(user_id: int) -> UserResponseBody:
    with create_session() as session:
        user = session.query(User).get(user_id)
        if not user:
            abort(404)
        return UserResponseBody.from_orm(user)


@users.route('/', methods=['POST'])
@validate()
def create_user() -> UserResponseBody:
    with create_session() as session:
        user = User()
        session.add(user)
        session.flush()
        return UserResponseBody.from_orm(user)


@users.route('/', methods=['GET'])
@validate(response_many=True)
def list_users() -> List[UserResponseBody]:
    with create_session() as session:
        users = session.query(User).all()
        return [UserResponseBody.from_orm(user) for user in users]


@users.route('/<int:user_id>/currencies/<int:currency_id>/', methods=['GET'])
@validate()
def get_user_currency(user_id: int, currency_id: int) -> UserCurrencyResponseBody:
    with create_session() as session:
        user = session.query(User).get(user_id)
        if not user:
            abort(404)
        currency = session.query(Currency).get(currency_id)
        if not currency:
            abort(404)
        uc = (
            session.query(UserCurrency)
            .filter(UserCurrency.currency == currency, UserCurrency.user == user)
            .first()
        )
        if uc:
            return UserCurrencyResponseBody.from_orm(uc)
        return UserCurrencyResponseBody(currency_id=currency_id)


@users.route('/<int:user_id>/currencies/', methods=['GET'])
@validate(response_many=True)
def list_user_currencies(user_id: int) -> List[UserCurrencyResponseBody]:
    with create_session() as session:
        user = session.query(User).get(user_id)
        if not user:
            abort(404)
        return [
            UserCurrencyResponseBody.from_orm(currency) for currency in user.currencies
        ]


@users.route('/<int:user_id>/transactions/', methods=['GET'])
@validate(response_many=True)
def list_user_transactions(
    user_id: int, query: TransactionListQuery
) -> List[TransactionResponseBody]:
    with create_session() as session:
        user = session.query(User).get(user_id)
        if not user:
            abort(404)
        transactions = (
            session.query(Transaction)
            .filter(Transaction.user == user)
            .filter(Transaction.id > query.last_id)
            .limit(current_app.config['TRANSACTIONS_PER_PAGE'])
        )
        return [
            TransactionResponseBody.from_orm(transaction)
            for transaction in transactions
        ]
