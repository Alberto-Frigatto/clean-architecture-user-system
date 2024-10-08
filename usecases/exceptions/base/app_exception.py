from dataclasses import dataclass, field


@dataclass(kw_only=True)
class AppException(Exception):
    message: str
    name: str = field(init=False)
    scope: str = field(init=False)

    def __post_init__(self) -> None:
        self.name = self.__class__.__name__
        self.scope = self.__class__.__qualname__.split('.', maxsplit=1)[0]
