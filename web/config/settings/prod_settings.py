from web.config.settings.base import Settings


class ProdSettings(Settings):
    api_title: str = 'Frigatto - PRODUÇÃO'
    mongo_database: str = 'frigatto_app'
