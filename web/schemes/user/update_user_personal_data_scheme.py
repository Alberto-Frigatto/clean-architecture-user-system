from datetime import date
from typing import Annotated, Any

from pydantic import EmailStr, StringConstraints, field_validator

from usecases.dto.user import UpdateUserPersonalDataDto
from web.docs.examples.schemes.user_schemes import UpdateUserPersonalDataScheme_example
from web.schemes.base import InputScheme


class UpdateUserPersonalDataScheme(InputScheme):
    username: Annotated[
        str,
        StringConstraints(
            strict=True,
            strip_whitespace=True,
            min_length=10,
            max_length=50,
            pattern=r'^[a-zA-ZÀ-ÿç\s]+$',
        ),
    ]
    email: Annotated[
        EmailStr,
        StringConstraints(
            strip_whitespace=True,
            max_length=100,
        ),
    ]
    birth_date: date

    @field_validator('birth_date', mode='after')
    @classmethod
    def is_birth_date_valid(cls, birth_date: date) -> date:
        now: date = date.today()
        diff_in_days: int = (now - birth_date).days
        diff_in_years: float = diff_in_days / 365.25

        if diff_in_years >= 100:
            raise ValueError('A data de nascimento é inválida')

        return birth_date

    def to_dto(self) -> UpdateUserPersonalDataDto:
        return UpdateUserPersonalDataDto(
            username=self.username,
            email=self.email,
            birth_date=self.birth_date,
        )

    model_config: dict[str, Any] = {  # type: ignore
        'json_schema_extra': {
            'examples': [UpdateUserPersonalDataScheme_example],
        }
    }
