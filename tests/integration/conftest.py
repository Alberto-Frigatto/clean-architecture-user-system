import os
from collections.abc import AsyncGenerator

import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


@pytest_asyncio.fixture
async def motor_database() -> AsyncGenerator[AsyncIOMotorDatabase]:
    client: AsyncIOMotorClient = AsyncIOMotorClient(
        os.getenv('MONGO_URI', 'mongodb://localhost:27017'),
        uuidRepresentation='standard',
        timeoutMS=5000,
    )
    db: AsyncIOMotorDatabase = client['test']

    yield db

    collections: list[str] = await db.list_collection_names()
    for collection_name in collections:
        await db.drop_collection(collection_name)

    client.close()
