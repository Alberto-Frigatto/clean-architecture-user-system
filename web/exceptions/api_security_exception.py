from web.exceptions.base import ApiException


class ApiSecurityException:
    class MissingJwt(ApiException):
        def __init__(self) -> None:
            super().__init__(message='Token JWT não fornecido')

    class InvalidJwt(ApiException):
        def __init__(self) -> None:
            super().__init__(message='Token JWT inválido')

    class ExpiredJwt(ApiException):
        def __init__(self) -> None:
            super().__init__(message='Token JWT expirado')
