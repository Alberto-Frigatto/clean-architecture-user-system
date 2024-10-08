from abc import ABC, abstractmethod
from uuid import UUID

from domain.entities import User


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None: ...

    @abstractmethod
    async def update(self, user: User) -> None: ...
