from unittest.mock import AsyncMock, Mock

import pytest

from domain.entities import User
from usecases.auth import AuthenticateUserUsecase
from usecases.dto.auth import LoginDto
from usecases.exceptions import AuthException, UserException


@pytest.fixture
def usecase(user_repository: Mock, password_manager: Mock) -> AuthenticateUserUsecase:
    return AuthenticateUserUsecase(user_repository, password_manager)


@pytest.mark.asyncio
async def test_authenticate_user_success(
    usecase: AuthenticateUserUsecase,
    user_repository: Mock,
    password_manager: Mock,
    user_list: list[User],
) -> None:
    dto: LoginDto = LoginDto(
        email='adriano@locaweb.com',
        password='Windows#123',
    )

    original_user: User = user_list[0]
    user_repository.get_by_email = AsyncMock(return_value=original_user)

    password_manager.verify = Mock(return_value=True)

    authenticated_user: User = await usecase.execute(dto)

    assert authenticated_user.birth_date == original_user.birth_date
    assert authenticated_user.email == original_user.email
    assert authenticated_user.hashed_password == original_user.hashed_password
    assert authenticated_user.is_active
    assert authenticated_user.username == original_user.username
    assert authenticated_user.color_theme == original_user.color_theme
    assert authenticated_user.language == original_user.language
    assert authenticated_user.id == original_user.id
    assert authenticated_user.created_at == original_user.created_at

    user_repository.get_by_email.assert_called_once_with(dto.email)
    password_manager.verify.assert_called_once_with(
        dto.password, original_user.hashed_password
    )


@pytest.mark.asyncio
async def test_when_try_to_authenticate_user_with_invalid_email_raises_InvalidCredentials(
    usecase: AuthenticateUserUsecase,
    user_repository: Mock,
) -> None:
    dto: LoginDto = LoginDto(
        email='naoexiste@locaweb.com',
        password='Windows#123',
    )

    user_repository.get_by_email = AsyncMock(return_value=None)

    with pytest.raises(AuthException.InvalidCredentials):
        await usecase.execute(dto)

    user_repository.get_by_email.assert_called_once_with(dto.email)


@pytest.mark.asyncio
async def test_when_try_to_authenticate_user_with_invalid_password_raises_InvalidCredentials(
    usecase: AuthenticateUserUsecase,
    user_repository: Mock,
    password_manager: Mock,
    user_list: list[User],
) -> None:
    dto: LoginDto = LoginDto(
        email='adriano@locaweb.com',
        password='senhaerrada123',
    )

    original_user: User = user_list[0]
    user_repository.get_by_email = AsyncMock(return_value=original_user)
    password_manager.verify = Mock(return_value=False)

    with pytest.raises(AuthException.InvalidCredentials):
        await usecase.execute(dto)

    user_repository.get_by_email.assert_called_once_with(dto.email)
    password_manager.verify.assert_called_once_with(
        dto.password, original_user.hashed_password
    )


@pytest.mark.asyncio
async def test_when_try_to_authenticate_a_deactivated_user_raises_UserIsDeactivated(
    usecase: AuthenticateUserUsecase, user_repository: Mock, user_list: list[User]
) -> None:
    dto: LoginDto = LoginDto(
        email='adriano@locaweb.com',
        password='Windows#123',
    )

    original_user: User = user_list[1]
    user_repository.get_by_email = AsyncMock(return_value=original_user)

    with pytest.raises(UserException.UserIsDeactivated):
        await usecase.execute(dto)

    user_repository.get_by_email.assert_called_once_with(dto.email)
