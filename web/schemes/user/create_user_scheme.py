from datetime import date
from typing import Annotated

from pydantic import EmailStr, StringConstraints, field_validator

from domain.value_objects import ColorTheme, Language
from usecases.dto.user import CreateUserDto
from web.schemes.base import InputScheme


class CreateUserScheme(InputScheme):
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
    password: Annotated[
        str,
        StringConstraints(
            strict=True,
            strip_whitespace=True,
            min_length=8,
            max_length=100,
        ),
    ]
    birth_date: date
    color_theme: ColorTheme
    language: Language

    @field_validator('password', mode='after')
    @classmethod
    def password_has_necessary_chars(cls, password: str) -> str:
        has_uppercase = any(char.isupper() for char in password)
        has_lowercase = any(char.islower() for char in password)
        has_digit = any(char.isdigit() for char in password)
        has_special = any(char in "!@#$%&*()_+=-,.:;?/\\|" for char in password)

        if not all((has_uppercase, has_lowercase, has_digit, has_special)):
            raise ValueError('A senha não tem os caracteres necessários')

        return password

    @field_validator('birth_date', mode='after')
    @classmethod
    def is_birth_date_valid(cls, birth_date: date) -> date:
        now: date = date.today()
        diff_in_days: int = (now - birth_date).days
        diff_in_years: float = diff_in_days / 365.25

        if diff_in_years >= 100:
            raise ValueError('A data de nascimento é inválida')

        return birth_date

    def to_dto(self) -> CreateUserDto:
        return CreateUserDto(
            username=self.username,
            email=self.email,
            password=self.password,
            birth_date=self.birth_date,
            color_theme=self.color_theme,
            language=self.language,
        )
