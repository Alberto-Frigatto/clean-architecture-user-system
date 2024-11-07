from abc import ABC, abstractmethod


class IIdManager(ABC):
    @abstractmethod
    def generate(self) -> str: ...
