from datetime import datetime

import sqlalchemy as sa

from crypto_exchange.database import Base, SqliteDecimal


class Currency(Base):
    __tablename__ = 'currencies'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    selling_rate = sa.Column(SqliteDecimal(scale=2))
    buying_rate = sa.Column(SqliteDecimal(scale=2))
    updated_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return (
            f'Currency(id={self.id}, name={self.name}, '
            f'selling_rate={self.selling_rate}, '
            f'buying_rate={self.buying_rate}, updated_at={self.updated_at})'
        )
