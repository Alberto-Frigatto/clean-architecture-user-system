from collections.abc import Callable
from datetime import date, datetime
from typing import Any

import pytest

from adapters.id import Ulid


@pytest.fixture
def is_ulid() -> Callable[[Any], bool]:
    def is_ulid_function(value: Any) -> bool:
        try:
            Ulid(value)
            return True
        except (ValueError, TypeError):
            return False

    return is_ulid_function


@pytest.fixture
def from_ulid_to_bytes() -> Callable[[str], bytes]:
    def as_ulid_function(value: str) -> bytes:
        return bytes(Ulid(value))

    return as_ulid_function


@pytest.fixture
def is_datetime() -> Callable[[Any], bool]:
    def is_datetime_function(value: Any) -> bool:
        try:
            if isinstance(value, datetime):
                return True

            if not isinstance(value, str):
                raise ValueError

            datetime.fromisoformat(value)
            return True
        except ValueError:
            return False

    return is_datetime_function


@pytest.fixture
def normalize_datetime() -> Callable[[datetime], datetime]:
    def normalize_datetime_function(dt: datetime) -> datetime:
        return dt.replace(microsecond=0, tzinfo=None)

    return normalize_datetime_function


@pytest.fixture
def subtract_years_from_today() -> Callable[[int], date]:
    def subtract_years_from_today_function(subtract_years: int) -> date:
        return (today := date.today()).replace(
            year=today.year - subtract_years,
            day=28 if (today.month, today.day) == (2, 29) else today.day,
        )

    return subtract_years_from_today_function
