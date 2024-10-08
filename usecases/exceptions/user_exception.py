from uuid import UUID

from usecases.exceptions.base import AppException


class UserException:
    class UserAlreadyExists(AppException):
        def __init__(self, email: str) -> None:
            super().__init__(message=f'O usuário {email} já existe')

    class UserNotFound(AppException):
        def __init__(self, user_id: UUID) -> None:
            super().__init__(message=f'O usuário {user_id} não foi encontrado')

    class UserIsDeactivated(AppException):
        def __init__(self, email: str) -> None:
            super().__init__(message=f'O usuário {email} está desativado')

    class NewPasswordCantBeSameAsOld(AppException):
        def __init__(self, email: str) -> None:
            super().__init__(
                message=f'A nova senha do usuário {email} não pode ser igual à antiga'
            )

    class NewPasswordConfirmationMismatch(AppException):
        def __init__(self) -> None:
            super().__init__(
                message='A confirmação da nova senha não corresponde à senha fornecida'
            )

    class OldPasswordDoesntMatch(AppException):
        def __init__(self) -> None:
            super().__init__(message='A senha antiga fornecida não corresponde a real')

    class UserIsUnderage(AppException):
        def __init__(self) -> None:
            super().__init__(message='O usuário é menor de idade')
