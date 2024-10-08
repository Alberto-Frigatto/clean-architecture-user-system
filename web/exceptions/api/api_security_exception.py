from web.exceptions.api.base import ApiError


class ApiSecurityException:
    class MissingJwt(ApiError):
        def __init__(self) -> None:
            super().__init__(message='Token JWT não fornecido')

    class InvalidJwt(ApiError):
        def __init__(self) -> None:
            super().__init__(message='Token JWT inválido')

    class ExpiredJwt(ApiError):
        def __init__(self) -> None:
            super().__init__(message='Token JWT expirado')
