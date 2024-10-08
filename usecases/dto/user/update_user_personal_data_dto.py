from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, kw_only=True)
class UpdateUserPersonalDataDto:
    username: str
    email: str
    birth_date: date
