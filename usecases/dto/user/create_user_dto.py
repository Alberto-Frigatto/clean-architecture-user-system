from dataclasses import dataclass
from datetime import date

from domain.value_objects import ColorTheme, Language


@dataclass(frozen=True, kw_only=True)
class CreateUserDto:
    username: str
    email: str
    password: str
    birth_date: date
    color_theme: ColorTheme
    language: Language
