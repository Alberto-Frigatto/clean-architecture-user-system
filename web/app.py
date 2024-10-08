from fastapi import FastAPI

from web.config import (
    add_error_handlers,
    add_routes,
    config_di,
    is_app_in_production_mode,
)
from web.config.settings.base import Settings
from web.di import Di


def create_app() -> FastAPI:
    config_di(test=not is_app_in_production_mode())

    settings: Settings = Di.get_raw(Settings)
    app: FastAPI = FastAPI(
        title=settings.api_title,
        debug=not is_app_in_production_mode(),
    )

    add_error_handlers(app)
    add_routes(app)

    return app
