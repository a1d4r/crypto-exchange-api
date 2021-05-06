from decimal import Decimal

from crypto_exchange.app import create_app
from crypto_exchange.currencies.models import Currency
from crypto_exchange.database import create_session
from crypto_exchange.users.models import User, UserCurrency


def fill_database() -> None:
    with create_session() as session:
        user1 = User(balance=Decimal('5435.29'))
        user2 = User(balance=Decimal('1000.00'))
        currency1 = Currency(
            name='Bitcoin',
            selling_rate=Decimal('504.54'),
            buying_rate=Decimal('632.53'),
        )
        currency2 = Currency(
            name='Ethereum',
            selling_rate=Decimal('243.10'),
            buying_rate=Decimal('323.84'),
        )
        currency3 = Currency(
            name='Dogecoin',
            selling_rate=Decimal('653.09'),
            buying_rate=Decimal('542.43'),
        )
        currency4 = Currency(
            name='Litecoin',
            selling_rate=Decimal('103.16'),
            buying_rate=Decimal('134.64'),
        )
        currency5 = Currency(
            name='Ripple', selling_rate=Decimal('375.28'), buying_rate=Decimal('465.19')
        )
        user1_currency1 = UserCurrency(
            user=user1, currency=currency1, amount=Decimal('10.58')
        )
        user2_currency2 = UserCurrency(
            user=user2, currency=currency2, amount=Decimal('20.36')
        )

        session.add_all(
            [
                user1,
                user2,
                currency1,
                currency2,
                currency3,
                currency4,
                currency5,
                user1_currency1,
                user2_currency2,
            ]
        )
        session.flush()


if __name__ == '__main__':
    create_app('migration')
    fill_database()
