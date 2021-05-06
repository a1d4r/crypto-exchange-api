from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from crypto_exchange.currencies.models import Currency
from crypto_exchange.transactions.models import Transaction, TransactionType
from crypto_exchange.users.models import User, UserCurrency


def test_user(session: Session):
    user = User()
    session.add(user)
    session.commit()
    assert user.id == 1
    assert user.balance == Decimal('1000.00')


def test_currency(session: Session):
    currency = Currency(
        name='currency', selling_rate=Decimal('12.34'), buying_rate=Decimal('56.78')
    )
    session.add(currency)
    session.commit()
    assert currency.name == 'currency'
    assert currency.selling_rate == Decimal('12.34')
    assert currency.buying_rate == Decimal('56.78')


def test_user_currency(session: Session):
    user = User()
    currency = Currency(
        name='currency', selling_rate=Decimal('12.34'), buying_rate=Decimal('56.78')
    )
    uc = UserCurrency(user=user, currency=currency, amount=Decimal('11.11'))
    session.add_all([user, currency, uc])
    session.commit()
    assert uc.user == user
    assert uc.currency == currency
    assert uc.user_id == user.id
    assert uc.currency_id == currency.id
    assert uc.amount == Decimal('11.11')


def test_transaction(session: Session):
    user = User()
    currency = Currency(
        name='currency', selling_rate=Decimal('12.34'), buying_rate=Decimal('56.78')
    )
    transaction = Transaction(
        user=user, currency=currency, type=TransactionType.BUY, amount=Decimal('11.11')
    )
    session.add_all([user, currency, transaction])
    session.commit()
    assert transaction.user == user
    assert transaction.currency == currency
    assert transaction.user_id == user.id
    assert transaction.currency_id == currency.id
    assert transaction.amount == Decimal('11.11')
    assert transaction.created_at <= datetime.now()
