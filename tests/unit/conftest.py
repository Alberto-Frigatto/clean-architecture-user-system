from collections.abc import Callable
from datetime import date
from typing import Any
from unittest.mock import Mock, create_autospec

import pytest

from domain.entities import User
from domain.value_objects import ColorTheme, Language
from ports.repositories.user import IUserRepository
from ports.security import IPasswordManager


@pytest.fixture
def user_list(subtract_years_from_today: Callable[[Any], date]) -> list[User]:
    return [
        User(
            birth_date=subtract_years_from_today(18),
            email='alberto@gmail.com',
            hashed_password='hashedpassword',
            username='Alberto Frigatto',
            color_theme=ColorTheme.LIGHT,
            language=Language.EN_UK,
        ),
        User(
            birth_date=subtract_years_from_today(33),
            email='leandro@hotmail.com.br',
            hashed_password='hashedpassword2',
            username='Leandro Nogueira',
            is_active=False,
            color_theme=ColorTheme.DARK,
            language=Language.PT_BR,
        ),
    ]


@pytest.fixture
def user_repository() -> Mock:
    return create_autospec(IUserRepository)


@pytest.fixture
def password_manager() -> Mock:
    return create_autospec(IPasswordManager)
