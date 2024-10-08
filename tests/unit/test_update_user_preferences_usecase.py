from unittest.mock import Mock

import pytest

from domain.entities import User
from domain.value_objects import ColorTheme, Language
from usecases.dto.user import UpdateUserPreferencesDto
from usecases.exceptions import UserException
from usecases.user import UpdateUserPreferencesUsecase


@pytest.fixture
def usecase(user_repository: Mock) -> UpdateUserPreferencesUsecase:
    return UpdateUserPreferencesUsecase(user_repository)


@pytest.mark.asyncio
async def test_update_user_preferences_success(
    usecase: UpdateUserPreferencesUsecase,
    user_repository: Mock,
    user_list: list[User],
) -> None:
    original_user: User = user_list[0]
    dto: UpdateUserPreferencesDto = UpdateUserPreferencesDto(
        color_theme=ColorTheme.DARK,
        language=Language.EN_UK,
    )

    updated_user: User = await usecase.execute(original_user, dto)

    assert updated_user.birth_date == original_user.birth_date
    assert updated_user.email == original_user.email
    assert updated_user.hashed_password == original_user.hashed_password
    assert updated_user.is_active
    assert updated_user.username == original_user.username
    assert updated_user.color_theme == dto.color_theme
    assert updated_user.language == dto.language
    assert updated_user.id == original_user.id
    assert updated_user.created_at == original_user.created_at

    user_repository.update.assert_called_once_with(updated_user)
