from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class UpdateUserPasswordDto:
    old_password: str
    new_password: str
    confirm_new_password: str
