from datetime import date, datetime
from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest

from domain.entities import User
from domain.value_objects import ColorTheme, Language
from usecases.dto.user import CreateUserDto
from usecases.exceptions import UserException
from usecases.user import CreateUserUsecase


@pytest.fixture
def usecase(
    user_repository: Mock, password_manager: Mock, id_manager: Mock
) -> CreateUserUsecase:
    return CreateUserUsecase(user_repository, password_manager, id_manager)


@pytest.mark.asyncio
async def test_create_user_success(
    usecase: CreateUserUsecase,
    user_repository: Mock,
    password_manager: Mock,
    id_manager: Mock,
) -> None:
    dto: CreateUserDto = CreateUserDto(
        birth_date=date(year=1989, month=6, day=27),
        email='adriano@locaweb.com',
        password='Windows#123',
        username='Adriano Lombardi',
        color_theme=ColorTheme.DARK,
        language=Language.PT_PT,
    )

    user_repository.get_by_email = AsyncMock(return_value=None)

    hashed_password: str = 'new_password'
    password_manager.hash = Mock(return_value=hashed_password)

    new_id: str = 'newid'
    id_manager.generate = Mock(return_value=new_id)

    created_user: User = await usecase.execute(dto)

    assert created_user.birth_date == dto.birth_date
    assert created_user.email == dto.email
    assert created_user.hashed_password == password_manager.hash.return_value
    assert created_user.is_active
    assert created_user.username == dto.username
    assert created_user.color_theme == dto.color_theme
    assert created_user.language == dto.language
    assert created_user.id == new_id
    assert isinstance(created_user.created_at, datetime)

    user_repository.get_by_email.assert_called_once_with(dto.email)
    user_repository.create.assert_called_once_with(created_user)
    password_manager.hash.assert_called_once_with(dto.password)
    id_manager.generate.assert_called_once()


@pytest.mark.asyncio
async def test_when_try_to_create_user_that_already_exists_raises_UserAlreadyExists(
    usecase: CreateUserUsecase, user_repository: Mock, user_list: list[User]
) -> None:
    dto: CreateUserDto = CreateUserDto(
        birth_date=date(year=1989, month=6, day=27),
        email='adriano@locaweb.com',
        password='Windows#123',
        username='Adriano Lombardi',
        color_theme=ColorTheme.LIGHT,
        language=Language.EN_US,
    )

    with pytest.raises(UserException.UserAlreadyExists):
        user_repository.get_by_email = AsyncMock(return_value=user_list[0])

        await usecase.execute(dto)

    user_repository.get_by_email.assert_called_once_with(dto.email)


@pytest.mark.asyncio
async def test_when_try_to_create_a_underage_user_raises_UserIsUnderAge(
    usecase: CreateUserUsecase, user_repository: Mock
) -> None:
    year: int = date.today().year - 10

    dto: CreateUserDto = CreateUserDto(
        birth_date=date(year=year, month=6, day=27),
        email='adriano@locaweb.com',
        password='Windows#123',
        username='Adriano Lombardi',
        color_theme=ColorTheme.LIGHT,
        language=Language.EN_US,
    )

    user_repository.get_by_email = AsyncMock(return_value=None)

    with pytest.raises(UserException.UserIsUnderage):
        await usecase.execute(dto)

    user_repository.get_by_email.assert_called_once_with(dto.email)
