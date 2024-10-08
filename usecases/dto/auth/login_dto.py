from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class LoginDto:
    email: str
    password: str
