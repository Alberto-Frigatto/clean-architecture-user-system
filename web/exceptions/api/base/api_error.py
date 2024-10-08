from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any


@dataclass(kw_only=True)
class ApiError(Exception):
    name: str = field(init=False)
    scope: str = field(init=False)
    message: str
    detail: Sequence[Any] | dict[str, Any] | None = field(default=None)

    def __post_init__(self) -> None:
        self.name = self.__class__.__name__
        self.scope = self.__class__.__qualname__.split('.', maxsplit=1)[0]
