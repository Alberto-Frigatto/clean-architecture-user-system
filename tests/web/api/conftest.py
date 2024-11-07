import asyncio
from collections.abc import AsyncGenerator, Callable

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorDatabase

from web.app import create_app
from web.di import Di


@pytest_asyncio.fixture(scope='session')
async def app_client() -> AsyncGenerator[AsyncClient]:
    app: FastAPI = create_app()
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest_asyncio.fixture(scope='function', loop_scope='function')
async def mongo_database() -> AsyncGenerator[AsyncIOMotorDatabase]:
    db: AsyncIOMotorDatabase = Di.get_raw(AsyncIOMotorDatabase)

    yield db

    collections: list[str] = await db.list_collection_names()
    for collection_name in collections:
        await db.drop_collection(collection_name)


@pytest.fixture(scope='session')
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except (RuntimeError, OSError):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    yield loop


@pytest.fixture
def authorization_header() -> Callable[[str], dict[str, str]]:
    def authorization_header_function(token: str) -> dict[str, str]:
        return {'Authorization': f'Bearer {token}'}

    return authorization_header_function
