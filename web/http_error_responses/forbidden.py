from http import HTTPStatus

from usecases.exceptions.base import AppException
from web.http_error_responses.base import HttpError


class Forbidden(HttpError):
    def __init__(
        self,
        error: AppException,
        *,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            error=error,
            headers=headers,
            status=HTTPStatus.FORBIDDEN,
        )
