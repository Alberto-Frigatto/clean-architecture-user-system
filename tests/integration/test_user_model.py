from datetime import date, datetime
from typing import Any

import pytest

from adapters.id import Ulid
from adapters.models import UserModel
from domain.entities import User


@pytest.fixture
def user_document(user: User) -> dict[str, Any]:
    return UserModel(**user.__dict__).to_document()


def test_create_UserModel_from_User_success(user: User):
    user_model: UserModel = UserModel(**user.__dict__)

    assert user_model.id == bytes(Ulid(user.id))
    assert user_model.birth_date == datetime(
        year=user.birth_date.year,
        month=user.birth_date.month,
        day=user.birth_date.day,
    )
    assert user_model.color_theme == user.color_theme
    assert user_model.created_at == user.created_at
    assert user_model.email == user.email
    assert user_model.hashed_password == user.hashed_password
    assert user_model.is_active == user.is_active
    assert user_model.language == user.language
    assert user_model.username == user.username


def test_map_UserModel_from_User_to_document_success(user: User):
    user_model: UserModel = UserModel(**user.__dict__)
    user_document: dict[str, Any] = user_model.to_document()

    assert isinstance(user_document, dict)
    assert user_document.get('_id') == bytes(Ulid(user.id))
    assert user_document.get('birth_date') == datetime(
        year=user.birth_date.year,
        month=user.birth_date.month,
        day=user.birth_date.day,
    )
    assert user_document.get('color_theme') == user.color_theme
    assert user_document.get('created_at') == user.created_at
    assert user_document.get('email') == user.email
    assert user_document.get('hashed_password') == user.hashed_password
    assert user_document.get('is_active') == user.is_active
    assert user_document.get('language') == user.language
    assert user_document.get('username') == user.username


def test_map_UserModel_from_document_to_User_success(user_document: dict[str, Any]):
    user_model: UserModel = UserModel(**user_document)
    user_entity: User = user_model.to_entity()

    assert isinstance(user_entity, User)

    assert user_entity.id == str(Ulid(user_document.get('_id')))

    birth_date: datetime | None = user_document.get('birth_date')
    assert birth_date is not None
    assert user_entity.birth_date == date(
        year=birth_date.year,
        month=birth_date.month,
        day=birth_date.day,
    )

    assert user_entity.color_theme == user_document.get('color_theme')
    assert user_entity.created_at == user_document.get('created_at')
    assert user_entity.email == user_document.get('email')
    assert user_entity.hashed_password == user_document.get('hashed_password')
    assert user_entity.is_active == user_document.get('is_active')
    assert user_entity.language == user_document.get('language')
    assert user_entity.username == user_document.get('username')
