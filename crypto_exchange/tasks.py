import atexit
from datetime import datetime
from random import randint

from apscheduler.schedulers.background import BackgroundScheduler

from crypto_exchange.currencies.models import Currency
from crypto_exchange.database import create_session


def start_scheduler() -> None:
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_currencies, 'interval', seconds=10)
    scheduler.start()
    atexit.register(scheduler.shutdown)


def update_currencies() -> None:
    with create_session() as session:
        currencies = session.query(Currency).all()
        for currency in currencies:
            currency.selling_rate += randint(-10, 10) * currency.selling_rate / 100
            currency.buying_rate += randint(-10, 10) * currency.buying_rate / 100
            currency.updated_at = datetime.utcnow()
            session.add(currency)
        session.commit()
        print('Currencies have been updated')
