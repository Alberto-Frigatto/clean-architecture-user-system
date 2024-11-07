from collections.abc import Sequence
from datetime import datetime, timezone
from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from usecases.exceptions.base import AppException


class HttpError:
    def __init__(
        self,
        *,
        error: AppException,
        status: int,
        headers: dict[str, str] | None,
    ) -> None:
        self._name: str = error.name
        self._scope: str = error.scope
        self._message: str = error.message
        self._detail: Sequence[Any] | dict[str, Any] | None = getattr(
            error, 'detail', None
        )
        self._type: str = self.__class__.__name__
        self._status: int = status
        self._headers: dict[str, str] | None = headers
        self._timestamp: str = datetime.now(timezone.utc).isoformat()

    def json(self) -> Response:
        return JSONResponse(
            content=jsonable_encoder(self._get_response_body()),
            status_code=self._status,
            headers=self._headers,
        )

    def _get_response_body(self) -> dict[str, Any]:
        return {
            key.removeprefix('_'): value
            for key, value in self.__dict__.items()
            if value is not None and key != '_headers'
        }
