from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

from usecases.exceptions.base import AppException


@dataclass(kw_only=True)
class ApiException(AppException):
    detail: Sequence[Any] | dict[str, Any] | None = field(default=None)
