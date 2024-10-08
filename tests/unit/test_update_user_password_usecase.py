from copy import deepcopy
from unittest.mock import Mock

import pytest

from domain.entities import User
from usecases.dto.user import UpdateUserPasswordDto
from usecases.exceptions import UserException
from usecases.user import UpdateUserPasswordUsecase


@pytest.fixture
def usecase(user_repository: Mock, password_manager: Mock) -> UpdateUserPasswordUsecase:
    return UpdateUserPasswordUsecase(user_repository, password_manager)


@pytest.mark.asyncio
async def test_update_user_password_success(
    usecase: UpdateUserPasswordUsecase,
    user_repository: Mock,
    password_manager: Mock,
    user_list: list[User],
) -> None:
    original_user: User = deepcopy(user_list[0])

    dto: UpdateUserPasswordDto = UpdateUserPasswordDto(
        old_password='hashedpassword',
        new_password='new_password',
        confirm_new_password='new_password',
    )

    password_manager.verify = Mock(return_value=True)
    password_manager.hash = Mock(return_value='nova_senha_criptografada')

    updated_user: User = await usecase.execute(original_user, dto)

    assert updated_user.birth_date == original_user.birth_date
    assert updated_user.email == original_user.email
    assert updated_user.hashed_password == password_manager.hash.return_value
    assert updated_user.is_active
    assert updated_user.username == original_user.username
    assert updated_user.color_theme == original_user.color_theme
    assert updated_user.language == original_user.language
    assert updated_user.id == original_user.id
    assert updated_user.created_at == original_user.created_at

    password_manager.verify.assert_called_once_with(
        dto.old_password, user_list[0].hashed_password
    )
    password_manager.hash.assert_called_once_with(dto.new_password)
    user_repository.update.assert_called_once_with(updated_user)


@pytest.mark.asyncio
async def test_when_try_to_update_user_password_with_old_password_that_does_not_match_the_real_one_raises_OldPasswordDoesntMatch(
    usecase: UpdateUserPasswordUsecase,
    password_manager: Mock,
    user_list: list[User],
) -> None:
    original_user: User = user_list[0]

    dto: UpdateUserPasswordDto = UpdateUserPasswordDto(
        old_password='senha_errada',
        new_password='new_password',
        confirm_new_password='new_password',
    )

    password_manager.verify = Mock(return_value=False)

    with pytest.raises(UserException.OldPasswordDoesntMatch):
        await usecase.execute(original_user, dto)


@pytest.mark.asyncio
async def test_when_try_to_update_user_password_with_confirm_new_password_that_does_not_match_new_password_raises_NewPasswordConfirmationMismatch(
    usecase: UpdateUserPasswordUsecase,
    password_manager: Mock,
    user_list: list[User],
) -> None:
    original_user: User = user_list[0]

    dto: UpdateUserPasswordDto = UpdateUserPasswordDto(
        old_password='hashedpassword',
        new_password='new_password',
        confirm_new_password='new_password2',
    )

    password_manager.verify = Mock(return_value=True)

    with pytest.raises(UserException.NewPasswordConfirmationMismatch):
        await usecase.execute(original_user, dto)


@pytest.mark.asyncio
async def test_when_try_to_update_user_password_with_new_password_being_same_as_old_password_raises_NewPasswordCantBeSameAsOld(
    usecase: UpdateUserPasswordUsecase,
    password_manager: Mock,
    user_list: list[User],
) -> None:
    original_user: User = user_list[0]

    dto: UpdateUserPasswordDto = UpdateUserPasswordDto(
        old_password='hashedpassword',
        new_password='hashedpassword',
        confirm_new_password='hashedpassword',
    )

    password_manager.verify = Mock(return_value=True)

    with pytest.raises(UserException.NewPasswordCantBeSameAsOld):
        await usecase.execute(original_user, dto)
