from datetime import date, datetime
from uuid import UUID

from pydantic import EmailStr

from domain.value_objects import ColorTheme, Language
from web.schemes.base import OutScheme


class UserOutScheme(OutScheme):
    id: UUID
    username: str
    email: EmailStr
    birth_date: date
    color_theme: ColorTheme
    language: Language
    is_active: bool
    created_at: datetime
