from web.exceptions.base import ApiException


class ApiSecurityException:
    class MissingJwt(ApiException):
        def __init__(self) -> None:
            super().__init__(message='JWT token not provided')

    class InvalidJwt(ApiException):
        def __init__(self) -> None:
            super().__init__(message='Invalid JWT token')

    class ExpiredJwt(ApiException):
        def __init__(self) -> None:
            super().__init__(message='Expired JWT token')
