from fastapi import FastAPI

from web.config import (
    add_error_handlers,
    add_middlewares,
    add_routes,
    config_di,
    is_app_in_production_mode,
)
from web.config.settings.base import Settings
from web.di import Di


def create_app() -> FastAPI:
    is_in_test = not is_app_in_production_mode()
    config_di(test=is_in_test)

    settings: Settings = Di.get_raw(Settings)
    app: FastAPI = FastAPI(
        title=settings.api_title,
        debug=is_in_test,
    )

    add_error_handlers(app)
    add_middlewares(app, test=is_in_test)
    add_routes(app)

    return app
