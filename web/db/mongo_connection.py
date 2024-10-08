from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from web.config.settings.base import Settings


class MongoConnection:
    @classmethod
    def get_client(cls, settings: Settings) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(
            settings.mongo_uri,
            uuidRepresentation='standard',
            timeoutMS=3000,
        )

    @classmethod
    def get_db(
        cls, client: AsyncIOMotorClient, settings: Settings
    ) -> AsyncIOMotorDatabase:
        db: AsyncIOMotorDatabase = client[settings.mongo_database]

        return db
