from http import HTTPStatus

from fastapi import APIRouter, Depends

from domain.entities import User
from usecases.user import (
    CreateUserUsecase,
    DeactivateUserUsecase,
    UpdateUserPasswordUsecase,
    UpdateUserPersonalDataUsecase,
    UpdateUserPreferencesUsecase,
)
from web.di import Di
from web.schemes.user import (
    CreateUserScheme,
    UpdateUserPasswordScheme,
    UpdateUserPersonalDataScheme,
    UpdateUserPreferencesScheme,
    UserOutScheme,
)
from web.utils.auth import AuthUtils


class UserController:
    router: APIRouter = APIRouter(prefix='/users', tags=['Users'])

    @staticmethod
    @router.post('/', status_code=HTTPStatus.CREATED)
    async def create_user(
        user: CreateUserScheme,
        usecase: CreateUserUsecase = Di.inject(CreateUserUsecase),
    ) -> UserOutScheme:
        new_user: User = await usecase.execute(user.to_dto())

        return UserOutScheme.from_entity(new_user)

    @staticmethod
    @router.get('/me', status_code=HTTPStatus.OK)
    async def get_user_info(
        auth_user: User = Depends(AuthUtils.get_auth_user),
    ) -> UserOutScheme:
        return UserOutScheme.from_entity(auth_user)

    @staticmethod
    @router.patch('/me/deactivate', status_code=HTTPStatus.NO_CONTENT)
    async def deactivate_user(
        auth_user: User = Depends(AuthUtils.get_auth_user),
        usecase: DeactivateUserUsecase = Di.inject(DeactivateUserUsecase),
    ) -> None:
        await usecase.execute(auth_user)

    @staticmethod
    @router.patch('/me/preferences', status_code=HTTPStatus.OK)
    async def update_user_preferences(
        preferences: UpdateUserPreferencesScheme,
        auth_user: User = Depends(AuthUtils.get_auth_user),
        usecase: UpdateUserPreferencesUsecase = Di.inject(UpdateUserPreferencesUsecase),
    ) -> UserOutScheme:
        updated_user: User = await usecase.execute(auth_user, preferences.to_dto())

        return UserOutScheme.from_entity(updated_user)

    @staticmethod
    @router.patch('/me', status_code=HTTPStatus.OK)
    async def update_user_personal_data(
        personal_data: UpdateUserPersonalDataScheme,
        auth_user: User = Depends(AuthUtils.get_auth_user),
        usecase: UpdateUserPersonalDataUsecase = Di.inject(
            UpdateUserPersonalDataUsecase
        ),
    ) -> UserOutScheme:
        updated_user: User = await usecase.execute(auth_user, personal_data.to_dto())

        return UserOutScheme.from_entity(updated_user)

    @staticmethod
    @router.patch('/me/password', status_code=HTTPStatus.OK)
    async def update_user_password(
        password_data: UpdateUserPasswordScheme,
        auth_user: User = Depends(AuthUtils.get_auth_user),
        usecase: UpdateUserPasswordUsecase = Di.inject(UpdateUserPasswordUsecase),
    ) -> UserOutScheme:
        updated_user: User = await usecase.execute(auth_user, password_data.to_dto())

        return UserOutScheme.from_entity(updated_user)
