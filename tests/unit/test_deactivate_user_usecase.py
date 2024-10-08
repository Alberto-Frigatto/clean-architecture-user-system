from unittest.mock import Mock

import pytest

from domain.entities import User
from usecases.user import DeactivateUserUsecase


@pytest.fixture
def usecase(user_repository: Mock) -> DeactivateUserUsecase:
    return DeactivateUserUsecase(user_repository)


@pytest.mark.asyncio
async def test_deactivate_user_success(
    usecase: DeactivateUserUsecase, user_repository: Mock, user_list: list[User]
) -> None:
    original_user: User = user_list[0]

    deactivated_user: User = await usecase.execute(original_user)

    assert deactivated_user.birth_date == original_user.birth_date
    assert deactivated_user.email == original_user.email
    assert deactivated_user.hashed_password == original_user.hashed_password
    assert not deactivated_user.is_active
    assert deactivated_user.username == original_user.username
    assert deactivated_user.color_theme == original_user.color_theme
    assert deactivated_user.language == original_user.language
    assert deactivated_user.id == original_user.id
    assert deactivated_user.created_at == original_user.created_at

    user_repository.update.assert_called_once_with(deactivated_user)
