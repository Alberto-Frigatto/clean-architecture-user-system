from typing import Annotated

from pydantic import EmailStr, StringConstraints

from usecases.dto.auth import LoginDto
from web.schemes.base import InputScheme


class AuthUserScheme(InputScheme):
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

    def to_dto(self) -> LoginDto:
        return LoginDto(email=self.email, password=self.password)
