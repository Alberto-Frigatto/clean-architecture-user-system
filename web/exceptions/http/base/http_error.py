from collections.abc import Sequence
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(kw_only=True, frozen=True)
class HttpError(Exception):
    name: str
    scope: str
    kind: str
    message: str
    status: int
    detail: Sequence[Any] | dict[str, Any] | None
    headers: dict[str, str] | None
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def json(self) -> dict[str, str | int]:
        serialization: dict = deepcopy(self.__dict__)

        del serialization['headers']

        if serialization.get('detail') is None:
            del serialization['detail']

        return serialization
