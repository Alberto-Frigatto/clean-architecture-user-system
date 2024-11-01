import os
from collections.abc import AsyncGenerator
from datetime import date

import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from domain.entities import User
from domain.value_objects import ColorTheme, Language


@pytest_asyncio.fixture
async def motor_database() -> AsyncGenerator[AsyncIOMotorDatabase]:
    client: AsyncIOMotorClient = AsyncIOMotorClient(
        os.getenv('MONGO_URI'),
        timeoutMS=3000,
    )
    db: AsyncIOMotorDatabase = client['test']

    yield db

    collections: list[str] = await db.list_collection_names()
    for collection_name in collections:
        await db.drop_collection(collection_name)


@pytest.fixture
def user() -> User:
    return User(
        id='01JAZR9WGHX847Q382GV068JRS',
        username='Alberto Frigatto',
        email='alberto@gmail.com',
        hashed_password='senha_criptografada',
        birth_date=date(year=2005, month=2, day=27),
        color_theme=ColorTheme.DARK,
        language=Language.PT_BR,
    )
