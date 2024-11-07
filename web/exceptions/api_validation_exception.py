from typing import Any, Sequence

from web.exceptions.base import ApiException


class ApiValidationException:
    class InvalidDataSent(ApiException):
        def __init__(
            self, detail: Sequence[Any] | dict[str, Any] | None = None
        ) -> None:
            super().__init__(message='Invalid data sent', detail=detail)
