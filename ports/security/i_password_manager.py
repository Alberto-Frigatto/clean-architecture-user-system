from abc import ABC, abstractmethod


class IPasswordManager(ABC):
    @abstractmethod
    def verify(self, plain_password: str, hashed_password: str) -> bool: ...

    @abstractmethod
    def hash(self, password: str) -> str: ...
