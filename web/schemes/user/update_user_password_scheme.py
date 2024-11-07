from typing import Annotated, Any

from pydantic import StringConstraints, field_validator

from usecases.dto.user import UpdateUserPasswordDto
from web.docs.examples.schemes.user_schemes import UpdateUserPasswordScheme_example
from web.schemes.base import InputScheme
from web.schemes.exceptions.user import UserSchemeException


class UpdateUserPasswordScheme(InputScheme):
    old_password: Annotated[
        str,
        StringConstraints(
            strict=True,
            strip_whitespace=True,
            min_length=8,
            max_length=100,
        ),
    ]
    new_password: Annotated[
        str,
        StringConstraints(
            strict=True,
            strip_whitespace=True,
            min_length=8,
            max_length=100,
        ),
    ]
    confirm_new_password: Annotated[
        str,
        StringConstraints(
            strict=True,
            strip_whitespace=True,
            min_length=8,
            max_length=100,
        ),
    ]

    @field_validator('new_password', 'confirm_new_password', mode='after')
    @classmethod
    def password_has_necessary_chars(cls, password: str) -> str:
        has_uppercase = any(char.isupper() for char in password)
        has_lowercase = any(char.islower() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_special = any(char in "!@#$%&*()_+=-,.:;?/\\|" for char in password)

        if not all((has_uppercase, has_lowercase, has_digit, has_special)):
            raise UserSchemeException.PasswordHasNoNecessaryChars()

        return password

    def to_dto(self) -> UpdateUserPasswordDto:
        return UpdateUserPasswordDto(
            old_password=self.old_password,
            new_password=self.new_password,
            confirm_new_password=self.confirm_new_password,
        )

    model_config: dict[str, Any] = {  # type: ignore
        'json_schema_extra': {
            'examples': [UpdateUserPasswordScheme_example],
        }
    }
