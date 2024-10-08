from uuid import UUID

from domain.entities import User
from ports.repositories.user import IUserRepository
from usecases.exceptions import UserException


class GetActiveUserUsecase:
    def __init__(self, repository: IUserRepository) -> None:
        self._repository: IUserRepository = repository

    async def execute(self, user_id: UUID) -> User:
        user: User | None = await self._repository.get_by_id(user_id)

        if user is None:
            raise UserException.UserNotFound(user_id)

        if not user.is_active:
            raise UserException.UserIsDeactivated(user.email)

        return user
