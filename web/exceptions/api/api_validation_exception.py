from typing import Any, Sequence

from web.exceptions.api.base import ApiError


class ApiValidationException:
    class InvalidDataSent(ApiError):
        def __init__(
            self, detail: Sequence[Any] | dict[str, Any] | None = None
        ) -> None:
            super().__init__(message='Os dados enviados são inválidos', detail=detail)
