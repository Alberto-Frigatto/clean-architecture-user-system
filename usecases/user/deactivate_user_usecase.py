from domain.entities import User
from ports.repositories.user import IUserRepository


class DeactivateUserUsecase:
    def __init__(self, repository: IUserRepository) -> None:
        self._repository: IUserRepository = repository

    async def execute(self, active_user: User) -> User:
        active_user.deactivate()

        await self._repository.update(active_user)

        return active_user
