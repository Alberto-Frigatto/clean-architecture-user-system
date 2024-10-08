from datetime import date

from domain.entities import User
from ports.repositories.user import IUserRepository
from usecases.dto.user import UpdateUserPersonalDataDto
from usecases.exceptions import UserException


class UpdateUserPersonalDataUsecase:
    def __init__(self, repository: IUserRepository) -> None:
        self._repository: IUserRepository = repository

    async def execute(self, active_user: User, dto: UpdateUserPersonalDataDto) -> User:
        if self._is_user_underage(dto.birth_date):
            raise UserException.UserIsUnderage()

        active_user.update_personal_data(
            new_username=dto.username,
            new_email=dto.email,
            new_birth_date=dto.birth_date,
        )

        await self._repository.update(active_user)

        return active_user

    def _is_user_underage(self, birth_date: date) -> bool:
        legal_age_date: date = (today := date.today()).replace(
            year=today.year - 18,
            day=28 if (today.month, today.day) == (2, 29) else today.day,
        )

        return birth_date > legal_age_date
