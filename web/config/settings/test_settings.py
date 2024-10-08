from web.config.settings.base import Settings


class TestSettings(Settings):
    api_title: str = 'Frigatto - TESTE'
    mongo_database: str = 'test'
    mongo_uri: str = 'mongodb://localhost:27017'
    secret_key: str = 'key'
