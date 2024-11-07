from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from domain.entities import User
from usecases.auth import AuthenticateUserUsecase
from web.di import Di
from web.docs.endpoints.auth import auth_endpoints
from web.schemes.auth import AuthUserScheme, TokenOutScheme
from web.security import IJwtManager


class AuthController:
    router: APIRouter = APIRouter(prefix='/auth', tags=['Authentication'])

    @staticmethod
    @router.post(
        '/token/',
        status_code=HTTPStatus.CREATED,
        description=auth_endpoints.authenticate_user_description,
    )
    async def authenticate_user(
        credentials: OAuth2PasswordRequestForm = Depends(),
        usecase: AuthenticateUserUsecase = Di.inject(AuthenticateUserUsecase),
        jwt_manager: IJwtManager = Di.inject(IJwtManager),
    ) -> TokenOutScheme:
        credentials_scheme: AuthUserScheme = AuthUserScheme(
            email=credentials.username,
            password=credentials.password,
        )
        user: User = await usecase.execute(credentials_scheme.to_dto())

        token: str = jwt_manager.create_access_token(user.id)

        return TokenOutScheme(access_token=token)
