from web.config.settings.base import Settings


class TestSettings(Settings):
    api_title: str = 'Frigatto - TESTE'
    mongo_database: str = 'test'
    secret_key: str = 'key'
