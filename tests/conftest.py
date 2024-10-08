from collections.abc import Callable
from datetime import date, datetime
from typing import Any
from uuid import UUID

import pytest


@pytest.fixture
def is_uuid() -> Callable[[Any], bool]:
    def is_uuid_function(value: Any) -> bool:
        try:
            if isinstance(value, UUID):
                return True

            if not isinstance(value, str):
                raise ValueError

            uuid_obj = UUID(value, version=4)
        except ValueError:
            return False

        return str(uuid_obj) == value

    return is_uuid_function


@pytest.fixture
def as_uuid() -> Callable[[str], UUID]:
    def as_uuid_function(value: str) -> UUID:
        return UUID(value, version=4)

    return as_uuid_function


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
