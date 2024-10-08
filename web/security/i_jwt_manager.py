from abc import ABC, abstractmethod
from uuid import UUID


class IJwtManager(ABC):
    @abstractmethod
    def create_access_token(self, sub: str) -> str: ...

    @abstractmethod
    def decode_access_token(self, token: str) -> dict[str, str]: ...

    @abstractmethod
    def get_sub(self, token: str) -> UUID: ...
