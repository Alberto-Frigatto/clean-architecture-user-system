from fastapi import Depends

from domain.entities import User
from usecases.user import GetActiveUserUsecase
from web.di import Di
from web.security import IJwtManager, oauth2_scheme


class AuthUtils:
    @staticmethod
    async def get_auth_user(
        token: str = Depends(oauth2_scheme),
        jwt_manager: IJwtManager = Di.inject(IJwtManager),
        usecase: GetActiveUserUsecase = Di.inject(GetActiveUserUsecase),
    ) -> User:
        user_id: str = jwt_manager.get_sub(token)
        user: User = await usecase.execute(user_id)

        return user
