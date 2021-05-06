import requests
import time

# Bot monitoring currency rates
# If at some moment selling rate is higher than buying rate, bot will abuse it
# to get as much money as it can

# For simplicity, exception handling is omitted


class ExchangeService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_currencies(self):
        r = requests.get(f'{self.base_url}/currencies/')
        return r.json()

    def get_currency(self, currency_id):
        r = requests.get(f'{self.base_url}/currencies/{currency_id}/')
        return r.json()


class Bot:
    def __init__(self, exchange_service: ExchangeService):
        self.exchange_service = exchange_service
        self.base_url = self.exchange_service.base_url
        self.user_id = self.register()

    def register(self):
        r = requests.post(f'{self.base_url}/users/')
        body = r.json()
        user_id = body['id']
        return user_id

    @property
    def balance(self):
        r = requests.get(f'{self.base_url}/users/{self.user_id}/')
        body = r.json()
        return body['balance']

    def main_loop(self):
        balance = self.balance
        print('Balance:', balance)
        while balance < 1_000_000:  # Until we become a millionaire
            currencies = self.exchange_service.get_currencies()

            for currency in currencies:
                if currency['buying_rate'] < currency['selling_rate']:  # buying and selling the same currency
                    amount = round(self.balance / currency['buying_rate'] - 0.005, 2)
                    self.buy_currency(currency['id'], amount)
                    self.sell_currency(currency['id'], amount)

            balance = self.balance
            print('Balance:', balance)
            time.sleep(1)

    def buy_currency(self, currency_id, amount):
        currency = self.exchange_service.get_currency(currency_id)
        r = requests.post(
            f'{self.base_url}/transactions/',
            json={
                'user_id': self.user_id,
                'currency_id': currency_id,
                'amount': amount,
                'type': 'buy',
                'currency_updated_at': currency['updated_at']
            }
        )

    def sell_currency(self, currency_id, amount):
        currency = self.exchange_service.get_currency(currency_id)
        r = requests.post(
            f'{self.base_url}/transactions/',
            json={
                'user_id': self.user_id,
                'currency_id': currency_id,
                'amount': amount,
                'type': 'sell',
                'currency_updated_at': currency['updated_at']
            }
        )


service = ExchangeService('http://127.0.0.1:5000')
bot = Bot(service)
bot.main_loop()
