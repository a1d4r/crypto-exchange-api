from decimal import Decimal
from enum import Enum

import sqlalchemy as sa
import sqlalchemy.orm as so

from crypto_exchange.config import GlobalConfig
from crypto_exchange.database import Base, SqliteDecimal

Numeric = SqliteDecimal(scale=GlobalConfig().DECIMAL_PRECISION)


class TransactionType(Enum):
    BUY = 'buy'
    SELL = 'sell'


class User(Base):

    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    balance = sa.Column(SqliteDecimal(scale=2), default=Decimal('1000.00'))
    currencies = so.relationship('UserCurrency', back_populates='user', lazy='dynamic')
    transactions = so.relationship('Transaction', back_populates='user', lazy='dynamic')

    def __repr__(self) -> str:
        return f'User(id={self.id}, balance={self.balance})'


class UserCurrency(Base):
    __tablename__ = 'user_currency'

    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), primary_key=True)
    currency_id = sa.Column(
        sa.Integer, sa.ForeignKey('currencies.id'), primary_key=True
    )
    amount = sa.Column(SqliteDecimal(scale=2), default=Decimal('0.00'))
    user = so.relationship('User', back_populates='currencies', lazy='select')
    currency = so.relationship('Currency', lazy='select')

    def __repr__(self) -> str:
        return (
            f'UserCurrency(user_id={self.user_id}, currency_id={self.currency_id}, '
            f'amount={self.amount})'
        )
