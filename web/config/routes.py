from fastapi import FastAPI

from web.controllers import AuthController, UserController


def add_routes(app: FastAPI) -> None:
    app.include_router(UserController.router)
    app.include_router(AuthController.router)
