from datetime import date

from domain.entities import User
from ports.id import IIdManager
from ports.repositories.user import IUserRepository
from ports.security import IPasswordManager
from usecases.dto.user import CreateUserDto
from usecases.exceptions import UserException


class CreateUserUsecase:
    def __init__(
        self,
        repository: IUserRepository,
        password_manager: IPasswordManager,
        id_manager: IIdManager,
    ) -> None:
        self._repository: IUserRepository = repository
        self._password_manager: IPasswordManager = password_manager
        self._id_manager: IIdManager = id_manager

    async def execute(self, dto: CreateUserDto) -> User:
        if await self._is_user_already_created(dto.email):
            raise UserException.UserAlreadyExists(dto.email)

        if self._is_user_underage(dto.birth_date):
            raise UserException.UserIsUnderage()

        hashed_password: str = self._password_manager.hash(dto.password)

        user: User = User(
            id=self._id_manager.generate(),
            birth_date=dto.birth_date,
            email=dto.email,
            hashed_password=hashed_password,
            username=dto.username,
            color_theme=dto.color_theme,
            language=dto.language,
        )

        await self._repository.create(user)

        return user

    async def _is_user_already_created(self, email: str) -> bool:
        return bool(await self._repository.get_by_email(email))

    def _is_user_underage(self, birth_date: date) -> bool:
        legal_age_date: date = (today := date.today()).replace(
            year=today.year - 18,
            day=28 if (today.month, today.day) == (2, 29) else today.day,
        )

        return birth_date > legal_age_date
