from datetime import date, datetime
from typing import Annotated
from uuid import UUID

from pydantic import ConfigDict, Field, field_validator

from adapters.models.base import MongoModel
from domain.entities import User
from domain.value_objects import ColorTheme, Language


class UserModel(MongoModel):
    id: Annotated[UUID, Field(serialization_alias='_id')]
    username: str
    email: str
    hashed_password: str
    birth_date: datetime
    color_theme: ColorTheme
    language: Language
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator('birth_date', mode='before')
    @classmethod
    def cast_birth_date(cls, birth_date: date) -> datetime:
        return datetime(
            year=birth_date.year,
            month=birth_date.month,
            day=birth_date.day,
        )

    def to_entity(self) -> User:
        return User(
            id=self.id,
            birth_date=date(
                year=self.birth_date.year,
                month=self.birth_date.month,
                day=self.birth_date.day,
            ),
            color_theme=self.color_theme,
            created_at=self.created_at,
            email=self.email,
            hashed_password=self.hashed_password,
            is_active=self.is_active,
            language=self.language,
            username=self.username,
        )
