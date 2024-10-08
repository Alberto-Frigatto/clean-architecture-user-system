from fastapi import FastAPI

from web.app import create_app

app: FastAPI = create_app()
