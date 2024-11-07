from adapters.id import Ulid
from ports.id import IIdManager


class UlidManager(IIdManager):
    def generate(self) -> str:
        return str(Ulid())
