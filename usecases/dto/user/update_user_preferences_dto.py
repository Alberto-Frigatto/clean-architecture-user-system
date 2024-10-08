from dataclasses import dataclass

from domain.value_objects import ColorTheme, Language


@dataclass(frozen=True, kw_only=True)
class UpdateUserPreferencesDto:
    color_theme: ColorTheme
    language: Language
