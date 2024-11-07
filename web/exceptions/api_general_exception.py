from web.exceptions.base import ApiException


class ApiGeneralException:
    class EndpointNotFound(ApiException):
        def __init__(self, endpoint: str) -> None:
            super().__init__(message=f'The endpoint {endpoint} doesn\'t exists')

    class MethodNotAllowed(ApiException):
        def __init__(self, *, method: str, endpoint: str) -> None:
            super().__init__(
                message=f'The {method} method isn\'t allowed for the endpoint {endpoint}'
            )
