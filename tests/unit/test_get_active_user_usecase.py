from unittest.mock import AsyncMock, Mock
from uuid import UUID, uuid4

import pytest

from domain.entities import User
from usecases.exceptions import UserException
from usecases.user import GetActiveUserUsecase


@pytest.fixture
def usecase(user_repository: Mock) -> GetActiveUserUsecase:
    return GetActiveUserUsecase(user_repository)


@pytest.mark.asyncio
async def test_get_active_user_success(
    usecase: GetActiveUserUsecase,
    user_repository: Mock,
    user_list: list[User],
) -> None:
    original_user: User = user_list[0]
    user_repository.get_by_id = AsyncMock(return_value=original_user)

    user: User = await usecase.execute(original_user.id)

    assert user.birth_date == original_user.birth_date
    assert user.email == original_user.email
    assert user.hashed_password == original_user.hashed_password
    assert user.is_active
    assert user.username == original_user.username
    assert user.color_theme == original_user.color_theme
    assert user.language == original_user.language
    assert user.id == original_user.id
    assert user.created_at == original_user.created_at

    user_repository.get_by_id.assert_called_once_with(original_user.id)


@pytest.mark.asyncio
async def test_when_try_to_get_an_active_user_that_does_not_exist_raises_UserNotFound(
    usecase: GetActiveUserUsecase,
    user_repository: Mock,
) -> None:
    user_repository.get_by_id = AsyncMock(return_value=None)

    user_id: UUID = uuid4()

    with pytest.raises(UserException.UserNotFound):
        await usecase.execute(user_id)

    user_repository.get_by_id.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_when_try_to_get_a_deactivated_user_raises_UserIsDeactivated(
    usecase: GetActiveUserUsecase,
    user_repository: Mock,
    user_list: list[User],
) -> None:
    original_user: User = user_list[1]
    user_repository.get_by_id = AsyncMock(return_value=original_user)

    with pytest.raises(UserException.UserIsDeactivated):
        await usecase.execute(original_user.id)

    user_repository.get_by_id.assert_called_once_with(original_user.id)
