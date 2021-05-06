from contextlib import contextmanager
from decimal import Decimal
from typing import Any

from flask import Flask
from sqlalchemy import Integer, TypeDecorator, create_engine
from sqlalchemy.engine import Dialect
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as SessionClass

Base: DeclarativeMeta = declarative_base()
Session = sessionmaker()


def init_db(app: Flask) -> None:
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    if app.config.get('CREATE_TABLES', False):
        # make sure all SQLAlchemy models are loaded
        from crypto_exchange.currencies import models as currency_models  # noqa
        from crypto_exchange.transactions import models as transaction_models  # noqa
        from crypto_exchange.users import models as user_models  # noqa

        Base.metadata.create_all(engine)

    Session.configure(bind=engine)


@contextmanager
def create_session(**kwargs: Any) -> SessionClass:
    new_session = Session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


class SqliteDecimal(TypeDecorator):
    # This TypeDecorator use Sqlalchemy Integer as impl. It converts Decimals
    # from Python to Integers which is later stored in Sqlite database.
    impl = Integer

    def __init__(self, scale: int) -> None:
        # It takes a 'scale' parameter, which specifies the number of digits
        # to the right of the decimal point of the number in the column.
        TypeDecorator.__init__(self)
        self.scale = scale
        self.multiplier_int = 10 ** self.scale

    def process_bind_param(self, value: Any, dialect: Dialect) -> int:
        # e.g. value = Column(SqliteDecimal(2)) means a value such as
        # Decimal('12.34') will be converted to 1234 in Sqlite
        if value is not None:
            value = int(Decimal(value) * self.multiplier_int)
        return value

    def process_result_value(self, value: Any, dialect: Dialect) -> Decimal:
        # e.g. Integer 1234 in Sqlite will be converted to Decimal('12.34'),
        # when query takes place.
        if value is not None:
            value = Decimal(value) / self.multiplier_int
        return value
