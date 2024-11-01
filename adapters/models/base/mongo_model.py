from abc import ABC, abstractmethod
from typing import Any, Self

from pydantic import BaseModel, model_validator


class MongoModel(ABC, BaseModel):
    @abstractmethod
    def to_entity(self) -> Any: ...

    def to_document(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True)

    @classmethod
    def from_entity(cls, entity: Any) -> Self:
        return cls(**entity.__dict__)

    @classmethod
    def from_document(cls, document: dict[str, Any]) -> Self:
        return cls(**document)

    @model_validator(mode='before')
    @classmethod
    def rename_attrs(cls, data: dict[str, Any]) -> dict[str, Any]:
        data_with_renamed_keys: dict[str, Any] = {}

        for key, value in data.items():
            data_with_renamed_keys[key.removeprefix('_')] = value

        return data_with_renamed_keys
