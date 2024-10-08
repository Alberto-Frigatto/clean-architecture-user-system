from domain.entities import User
from ports.repositories.user import IUserRepository
from ports.security import IPasswordManager
from usecases.dto.auth import LoginDto
from usecases.exceptions import AuthException, UserException


class AuthenticateUserUsecase:
    def __init__(
        self,
        repository: IUserRepository,
        password_manager: IPasswordManager,
    ) -> None:
        self._repository: IUserRepository = repository
        self._password_manager: IPasswordManager = password_manager

    async def execute(self, dto: LoginDto) -> User:
        user: User | None = await self._repository.get_by_email(dto.email)

        if user is None or not self._password_manager.verify(
            dto.password, user.hashed_password
        ):
            raise AuthException.InvalidCredentials()

        if not user.is_active:
            raise UserException.UserIsDeactivated(user.email)

        return user
