from usecases.exceptions.base import AppException


class AuthException:
    class InvalidCredentials(AppException):
        def __init__(self) -> None:
            super().__init__(message='Email ou senha inválidos')
