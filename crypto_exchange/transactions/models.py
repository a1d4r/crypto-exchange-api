from datetime import datetime
from enum import Enum

import sqlalchemy as sa
import sqlalchemy.orm as so

from crypto_exchange.database import Base, SqliteDecimal


class TransactionType(Enum):
    BUY = 'buy'
    SELL = 'sell'


class Transaction(Base):
    __tablename__ = 'transactions'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    user = so.relationship('User', back_populates='transactions', lazy='select')
    currency_id = sa.Column(sa.Integer, sa.ForeignKey('currencies.id'))
    currency = so.relationship('Currency', lazy='select')
    amount = sa.Column(SqliteDecimal(scale=2))
    type = sa.Column(sa.Enum(TransactionType))
    created_at = sa.Column(sa.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return (
            f'Transaction(id={self.id}, user_id={self.user_id}, '
            f'currency_id={self.currency_id}, amount={self.amount}, '
            f'type={self.type}, created_at={self.created_at})'
        )
