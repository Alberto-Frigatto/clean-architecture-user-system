from datetime import date, datetime, timezone

from domain.value_objects import ColorTheme, Language


class User:
    def __init__(
        self,
        id: str,
        username: str,
        email: str,
        birth_date: date,
        hashed_password: str,
        color_theme: ColorTheme,
        language: Language,
        is_active: bool = True,
        created_at: datetime | None = None,
    ) -> None:
        self._id: str = id
        self._username: str = username
        self._email: str = email
        self._birth_date: date = birth_date
        self._hashed_password: str = hashed_password
        self._color_theme: ColorTheme = color_theme
        self._language: Language = language
        self._is_active: bool = is_active
        self._created_at: datetime = created_at or datetime.now(timezone.utc)

    def deactivate(self) -> None:
        self._is_active = False

    def update_password(self, new_hashed_password: str) -> None:
        self._hashed_password = new_hashed_password

    def update_personal_data(
        self, *, new_username: str, new_email: str, new_birth_date: date
    ) -> None:
        self._username = new_username
        self._email = new_email
        self._birth_date = new_birth_date

    def update_preferences(
        self, *, new_color_theme: ColorTheme, new_language: Language
    ) -> None:
        self._color_theme = new_color_theme
        self._language = new_language

    @property
    def username(self) -> str:
        return self._username

    @property
    def email(self) -> str:
        return self._email

    @property
    def birth_date(self) -> date:
        return self._birth_date

    @property
    def hashed_password(self) -> str:
        return self._hashed_password

    @property
    def color_theme(self) -> ColorTheme:
        return self._color_theme

    @property
    def language(self) -> Language:
        return self._language

    @property
    def id(self) -> str:
        return self._id

    @property
    def is_active(self) -> bool:
        return self._is_active

    @property
    def created_at(self) -> datetime:
        return self._created_at
