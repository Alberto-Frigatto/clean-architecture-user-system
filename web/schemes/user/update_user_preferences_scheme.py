from typing import Any

from domain.value_objects import ColorTheme, Language
from usecases.dto.user import UpdateUserPreferencesDto
from web.docs.examples.schemes.user_schemes import UpdateUserPreferencesScheme_example
from web.schemes.base import InputScheme


class UpdateUserPreferencesScheme(InputScheme):
    color_theme: ColorTheme
    language: Language

    def to_dto(self) -> UpdateUserPreferencesDto:
        return UpdateUserPreferencesDto(
            color_theme=self.color_theme,
            language=self.language,
        )

    model_config: dict[str, Any] = {  # type: ignore
        'json_schema_extra': {
            'examples': [UpdateUserPreferencesScheme_example],
        }
    }
