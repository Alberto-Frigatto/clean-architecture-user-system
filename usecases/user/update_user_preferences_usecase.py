from domain.entities import User
from ports.repositories.user import IUserRepository
from usecases.dto.user import UpdateUserPreferencesDto


class UpdateUserPreferencesUsecase:
    def __init__(self, repository: IUserRepository) -> None:
        self._repository: IUserRepository = repository

    async def execute(self, active_user: User, dto: UpdateUserPreferencesDto) -> User:
        active_user.update_preferences(
            new_color_theme=dto.color_theme,
            new_language=dto.language,
        )

        await self._repository.update(active_user)

        return active_user
