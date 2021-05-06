from typing import Optional

from flask import Flask

from crypto_exchange.config import GlobalConfig, get_config
from crypto_exchange.currencies.routes import currencies
from crypto_exchange.database import init_db
from crypto_exchange.tasks import start_scheduler
from crypto_exchange.transactions.routes import transactions
from crypto_exchange.users.routes import users


def create_app(config_name: Optional[str] = None) -> Flask:
    """Create app with the specified config. (or env FLASK_CONFIG if ommited)"""
    app = Flask(__name__)
    config_name = config_name or GlobalConfig().FLASK_CONFIG
    config = get_config(config_name)
    app.config.from_object(config)
    init_db(app)
    with app.app_context():
        app.register_blueprint(users, url_prefix='/users')
        app.register_blueprint(currencies, url_prefix='/currencies')
        app.register_blueprint(transactions, url_prefix='/transactions')
    return app


app = create_app()
start_scheduler()
