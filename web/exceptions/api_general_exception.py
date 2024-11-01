from web.exceptions.base import ApiException


class ApiGeneralException:
    class EndpointNotFound(ApiException):
        def __init__(self, endpoint: str) -> None:
            super().__init__(message=f'O endpoint {endpoint} não existe')

    class MethodNotAllowed(ApiException):
        def __init__(self, *, method: str, endpoint: str) -> None:
            super().__init__(
                message=f'O método {method} não é permitido para o endpoint {endpoint}'
            )
