from datetime import date, datetime
from typing import Any

from pydantic import EmailStr

from domain.value_objects import ColorTheme, Language
from web.docs.examples.schemes.user_schemes import UserOutScheme_example
from web.schemes.base import OutScheme


class UserOutScheme(OutScheme):
    id: str
    username: str
    email: EmailStr
    birth_date: date
    color_theme: ColorTheme
    language: Language
    is_active: bool
    created_at: datetime

    model_config: dict[str, Any] = {  # type: ignore
        'json_schema_extra': {
            'examples': [UserOutScheme_example],
        }
    }
