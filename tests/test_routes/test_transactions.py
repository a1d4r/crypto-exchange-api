from decimal import ROUND_DOWN, Decimal

from flask import Response
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from crypto_exchange.transactions.models import Transaction, TransactionType
from crypto_exchange.transactions.schemas import (
    CreateTransactionBody,
    TransactionListResponseBody,
    TransactionResponseBody,
)
from crypto_exchange.users.models import UserCurrency


def test_get_transactions(client: FlaskClient, transaction_factory):  # type: ignore
    transaction = transaction_factory()
    response: Response = client.get('/transactions/1/')
    assert response.status_code == 200

    actual_transaction = TransactionResponseBody.from_orm(transaction)
    retrieved_transaction = TransactionResponseBody.parse_raw(response.data)
    assert actual_transaction == retrieved_transaction


def test_list_transactions(client: FlaskClient, transaction_factory):  # type: ignore
    transactions = transaction_factory.create_batch(3)
    response: Response = client.get('/transactions/')
    assert response.status_code == 200

    actual_transactions = TransactionListResponseBody(__root__=transactions)
    retrieved_transactions = TransactionListResponseBody.parse_raw(response.data)
    assert actual_transactions == retrieved_transactions


def test_list_user_transactions(
    client: FlaskClient, user_factory, transaction_factory  # type: ignore
):
    user = user_factory()
    transactions = transaction_factory.create_batch(3, user=user)
    response: Response = client.get('/users/1/transactions/')
    assert response.status_code == 200

    actual_transactions = TransactionListResponseBody(__root__=transactions)
    retrieved_transactions = TransactionListResponseBody.parse_raw(response.data)
    assert actual_transactions == retrieved_transactions


def test_buy_currency(
    client: FlaskClient,  # type: ignore
    session: Session,
    user_factory,
    currency_factory,
    transaction_factory,
):
    # Prepare database
    old_balance = Decimal('1000000.00')
    user = user_factory(balance=old_balance)
    currency = currency_factory()
    request_transaction = CreateTransactionBody(
        user_id=user.id,
        currency_id=currency.id,
        amount=Decimal('1.23'),
        type=TransactionType.BUY,
        currency_updated_at=currency.updated_at,
    )
    payload = request_transaction.json().encode()

    # Check endpoint return 200
    response: Response = client.post('/transactions/', data=payload)
    assert response.status_code == 200

    # Check all data was saved correctly
    transaction = session.query(Transaction).get(1)
    requested_transaction = TransactionResponseBody(
        **request_transaction.dict(),
        id=transaction.id,
        created_at=transaction.created_at
    )
    actual_transaction = TransactionResponseBody.from_orm(transaction)
    retrieved_transaction = TransactionResponseBody.parse_raw(response.data)
    assert requested_transaction == actual_transaction == retrieved_transaction

    # Check right amount of currency was added
    uc = (
        session.query(UserCurrency)
        .filter(UserCurrency.user == user, UserCurrency.currency == currency)
        .first()
    )
    assert uc.amount == request_transaction.amount

    # Check balance was updated correctly
    session.refresh(user)
    expected_balance = (
        old_balance - request_transaction.amount * currency.buying_rate
    ).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    assert user.balance == expected_balance


def test_sell_currency(
    client: FlaskClient,  # type: ignore
    session: Session,
    user_factory,
    currency_factory,
    user_currency_factory,
    transaction_factory,
):
    # Prepare database
    old_balance = Decimal('1000000.00')
    user = user_factory(balance=old_balance)
    currency = currency_factory()

    old_amount = Decimal('2.00')
    uc = user_currency_factory(user=user, currency=currency, amount=old_amount)
    request_transaction = CreateTransactionBody(
        user_id=user.id,
        currency_id=currency.id,
        amount=Decimal('1.23'),
        type=TransactionType.SELL,
        currency_updated_at=currency.updated_at,
    )
    payload = request_transaction.json().encode()

    # Check endpoint return 200
    response: Response = client.post('/transactions/', data=payload)
    assert response.status_code == 200

    # Check all data was saved correctly
    transaction = session.query(Transaction).get(1)
    requested_transaction = TransactionResponseBody(
        **request_transaction.dict(),
        id=transaction.id,
        created_at=transaction.created_at
    )
    actual_transaction = TransactionResponseBody.from_orm(transaction)
    retrieved_transaction = TransactionResponseBody.parse_raw(response.data)
    assert requested_transaction == actual_transaction == retrieved_transaction

    # Check right amount of currency was subtracted
    uc = (
        session.query(UserCurrency)
        .filter(UserCurrency.user == user, UserCurrency.currency == currency)
        .first()
    )
    assert uc.amount == old_amount - request_transaction.amount

    # Check balance was updated correctly
    session.refresh(user)
    expected_balance = (
        old_balance + request_transaction.amount * currency.selling_rate
    ).quantize(Decimal('.01'), rounding=ROUND_DOWN)
    assert user.balance == expected_balance
