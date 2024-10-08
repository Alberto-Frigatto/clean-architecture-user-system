from collections.abc import Sequence
from http import HTTPStatus
from typing import Any

from web.exceptions.http.base import HttpError


class Forbidden(HttpError):
    def __init__(
        self,
        *,
        name: str,
        scope: str,
        message: str,
        detail: Sequence[Any] | dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            detail=detail,
            headers=headers,
            kind=self.__class__.__name__,
            message=message,
            name=name,
            scope=scope,
            status=HTTPStatus.FORBIDDEN,
        )
