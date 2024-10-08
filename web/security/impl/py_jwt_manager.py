from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from jwt.exceptions import ExpiredSignatureError

from web.config.settings.base import Settings
from web.exceptions.api import ApiSecurityException
from web.security import IJwtManager


class PyJwtManager(IJwtManager):
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def create_access_token(self, sub: str) -> str:
        expire: datetime = datetime.now(timezone.utc) + timedelta(
            minutes=self._settings.access_token_expire_minutes
        )
        payload: dict[str, str | datetime] = {
            'sub': sub,
            'exp': expire,
        }
        return jwt.encode(
            payload,
            self._settings.secret_key,
            algorithm=self._settings.jwt_algorithm,
        )

    def decode_access_token(self, token: str) -> dict[str, str]:
        try:
            return jwt.decode(
                token,
                self._settings.secret_key,
                algorithms=[self._settings.jwt_algorithm],
            )
        except ExpiredSignatureError as e:
            raise ApiSecurityException.ExpiredJwt() from e

    def get_sub(self, token: str) -> UUID:
        decoded_token: dict[str, str] = self.decode_access_token(token)

        try:
            return UUID(decoded_token['sub'], version=4)
        except ValueError as e:
            raise ApiSecurityException.InvalidJwt() from e
