from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class InputScheme(ABC, BaseModel):
    @abstractmethod
    def to_dto(self) -> Any: ...
