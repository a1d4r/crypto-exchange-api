from pydantic import BaseSettings, Field


class GlobalConfig(BaseSettings):
    DECIMAL_PRECISION: int = 2
    FLASK_CONFIG: str = Field('development', env='FLASK_CONFIG')
    SQLALCHEMY_DATABASE_URI: str = Field('sqlite:///crypto.db', env='DEV_DATABASE_URL')
    CREATE_TABLES: bool = False
    TRANSACTIONS_PER_PAGE: int = 10


class DevelopmentConfig(GlobalConfig):
    DEBUG: bool = True


class TestingConfig(GlobalConfig):
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI = Field('sqlite://')
    CREATE_TABLES: bool = True


class ProductionConfig(GlobalConfig):
    pass


class MigrationConfig(GlobalConfig):
    CREATE_TABLES: bool = True


configs = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'migration': MigrationConfig,
}


def get_config(config_name: str) -> GlobalConfig:
    return configs.get(config_name, DevelopmentConfig)()
