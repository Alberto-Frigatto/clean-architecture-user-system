from abc import ABC
from typing import Any, Self

from pydantic import BaseModel, model_validator


class OutScheme(ABC, BaseModel):
    @classmethod
    def from_entity(cls, entity: Any) -> Self:
        return cls(**entity.__dict__)

    @model_validator(mode='before')
    @classmethod
    def rename_attrs(cls, data: dict[str, Any]) -> dict[str, Any]:
        data_with_renamed_keys: dict[str, Any] = {}

        for key, value in data.items():
            data_with_renamed_keys[key.removeprefix('_')] = value

        return data_with_renamed_keys
