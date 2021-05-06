from decimal import Decimal

import factory

from crypto_exchange.currencies.models import Currency
from crypto_exchange.transactions.models import Transaction, TransactionType
from crypto_exchange.users.models import User, UserCurrency


def UserFactory(session):
    class ActualFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = User
            sqlalchemy_session = session
            sqlalchemy_session_persistence = 'commit'

        balance = Decimal('1000.00')

    return ActualFactory


def CurrencyFactory(session):
    class ActualFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Currency
            sqlalchemy_session = session
            sqlalchemy_session_persistence = 'commit'

        name = factory.Sequence(lambda n: f'Currency {n}')
        selling_rate = factory.Faker(
            'pydecimal', right_digits=2, positive=True, max_value=1_000
        )
        buying_rate = factory.Faker(
            'pydecimal', right_digits=2, positive=True, max_value=1_000
        )

    return ActualFactory


def UserCurrencyFactory(session):
    class ActualFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = UserCurrency
            sqlalchemy_session = session
            sqlalchemy_session_persistence = 'commit'

        user = factory.SubFactory(UserFactory(session))
        currency = factory.SubFactory(CurrencyFactory(session))
        amount = factory.Faker(
            'pydecimal', right_digits=2, positive=True, max_value=1_000
        )

    return ActualFactory


def TransactionFactory(session):
    class ActualFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Transaction
            sqlalchemy_session = session
            sqlalchemy_session_persistence = 'commit'

        user = factory.SubFactory(UserFactory(session))
        currency = factory.SubFactory(CurrencyFactory(session))
        amount = factory.Faker(
            'pydecimal', right_digits=2, positive=True, max_value=1_000
        )
        type = TransactionType.BUY

    return ActualFactory
