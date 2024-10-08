from datetime import date
from unittest.mock import Mock

import pytest

from domain.entities import User
from usecases.dto.user import UpdateUserPersonalDataDto
from usecases.exceptions import UserException
from usecases.user import UpdateUserPersonalDataUsecase


@pytest.fixture
def usecase(user_repository: Mock) -> UpdateUserPersonalDataUsecase:
    return UpdateUserPersonalDataUsecase(user_repository)


@pytest.mark.asyncio
async def test_update_user_personal_data_success(
    usecase: UpdateUserPersonalDataUsecase,
    user_repository: Mock,
    user_list: list[User],
) -> None:
    original_user: User = user_list[0]
    dto: UpdateUserPersonalDataDto = UpdateUserPersonalDataDto(
        username='Novo nome da silva',
        email='novoemail@gmail.com',
        birth_date=date(year=2005, month=2, day=27),
    )

    updated_user: User = await usecase.execute(original_user, dto)

    assert updated_user.birth_date == dto.birth_date
    assert updated_user.email == dto.email
    assert updated_user.hashed_password == original_user.hashed_password
    assert updated_user.is_active
    assert updated_user.username == dto.username
    assert updated_user.color_theme == original_user.color_theme
    assert updated_user.language == original_user.language
    assert updated_user.id == original_user.id
    assert updated_user.created_at == original_user.created_at

    user_repository.update.assert_called_once_with(updated_user)


@pytest.mark.asyncio
async def test_when_try_to_update_user_personal_data_with_underage_birth_date_raises_UserIsUnderage(
    usecase: UpdateUserPersonalDataUsecase,
    user_repository: Mock,
    user_list: list[User],
) -> None:
    original_user: User = user_list[0]
    dto: UpdateUserPersonalDataDto = UpdateUserPersonalDataDto(
        username='Novo nome da silva',
        email='novoemail@gmail.com',
        birth_date=date.today(),
    )

    with pytest.raises(UserException.UserIsUnderage):
        await usecase.execute(original_user, dto)
