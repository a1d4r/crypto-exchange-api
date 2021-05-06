from typing import List

from flask import Blueprint, abort, current_app
from flask_pydantic import validate

from crypto_exchange.currencies.models import Currency
from crypto_exchange.database import create_session
from crypto_exchange.users.models import User, UserCurrency

from .models import Transaction, TransactionType
from .schemas import (
    CreateTransactionBody,
    TransactionListQuery,
    TransactionResponseBody,
)

transactions = Blueprint('transactions', __name__)


@transactions.route('/<int:transaction_id>/', methods=['GET'])
@validate()
def get_transaction(transaction_id: int) -> TransactionResponseBody:
    with create_session() as session:
        transaction = session.query(Transaction).get(transaction_id)
        if not transaction:
            abort(404)
        return TransactionResponseBody.from_orm(transaction)


@transactions.route('/', methods=['GET'])
@validate(response_many=True)
def list_transaction(query: TransactionListQuery) -> List[TransactionResponseBody]:
    with create_session() as session:
        transactions = (
            session.query(Transaction)
            .filter(Transaction.id > query.last_id)
            .limit(current_app.config['TRANSACTIONS_PER_PAGE'])
        )
        return [
            TransactionResponseBody.from_orm(transaction)
            for transaction in transactions
        ]


@transactions.route('/', methods=['POST'])
@validate()
def create_transaction(body: CreateTransactionBody) -> TransactionResponseBody:
    with create_session() as session:
        # check if ids are valid
        user: User = session.query(User).get(body.user_id)
        if not user:
            abort(404, 'No user with such id')
        currency: Currency = session.query(Currency).get(body.currency_id)
        if not currency:
            abort(400, 'No currency with such id')

        if currency.updated_at != body.currency_updated_at:
            abort(400, 'Currency timestamp is outdated')

        # get user-currency association object
        uc = (
            session.query(UserCurrency)
            .filter(UserCurrency.currency == currency, UserCurrency.user == user)
            .first()
        )
        if not uc:
            uc = UserCurrency(user=user, currency=currency)
            session.add(uc)
            session.flush()

        if body.type == TransactionType.BUY:
            cost = currency.buying_rate * body.amount
            # check if user has enough money
            if cost > user.balance:
                abort(400, 'Not enough money')

            # update balance
            uc.amount += body.amount
            user.balance -= cost

        else:  # SELL
            profit = currency.selling_rate * body.amount
            # check if user has enough currency
            if body.amount > uc.amount:
                abort(400, 'Not enough currency')

            # update balance
            uc.amount -= body.amount
            user.balance += profit

        # create transaction
        transaction = Transaction(
            amount=body.amount, user=user, currency=currency, type=body.type
        )
        session.add_all([uc, user, transaction])
        session.flush()

        return TransactionResponseBody.from_orm(transaction)
