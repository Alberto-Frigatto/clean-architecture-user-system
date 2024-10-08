from typing import Any
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from adapters.models import UserModel
from domain.entities import User
from ports.repositories.user import IUserRepository


class MongoUserRepository(IUserRepository):
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._collection: AsyncIOMotorCollection = db['users']

    async def create(self, user: User) -> None:
        user_model: UserModel = UserModel.from_entity(user)

        await self._collection.insert_one(user_model.to_document())

    async def get_by_email(self, email: str) -> User | None:
        user: dict[str, Any] | None = await self._collection.find_one({'email': email})

        if user is None:
            return None

        return UserModel.from_document(user).to_entity()

    async def get_by_id(self, user_id: UUID) -> User | None:
        user: dict[str, Any] | None = await self._collection.find_one({'_id': user_id})

        if user is None:
            return None

        return UserModel.from_document(user).to_entity()

    async def update(self, user: User) -> None:
        user_model: UserModel = UserModel.from_entity(user)

        await self._collection.replace_one(
            {'_id': user_model.id}, user_model.to_document()
        )
