from domain.entities import User
from ports.repositories.user import IUserRepository
from ports.security import IPasswordManager
from usecases.dto.user import UpdateUserPasswordDto
from usecases.exceptions import UserException


class UpdateUserPasswordUsecase:
    def __init__(
        self, repository: IUserRepository, password_manager: IPasswordManager
    ) -> None:
        self._repository: IUserRepository = repository
        self._password_manager: IPasswordManager = password_manager

    async def execute(self, active_user: User, dto: UpdateUserPasswordDto) -> User:
        if not self._password_manager.verify(
            dto.old_password, active_user.hashed_password
        ):
            raise UserException.OldPasswordDoesntMatch()

        if dto.new_password != dto.confirm_new_password:
            raise UserException.NewPasswordConfirmationMismatch()

        if dto.new_password == dto.old_password:
            raise UserException.NewPasswordCantBeSameAsOld(active_user.email)

        active_user.update_password(self._password_manager.hash(dto.new_password))

        await self._repository.update(active_user)

        return active_user
