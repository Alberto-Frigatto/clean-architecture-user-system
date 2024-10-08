from collections.abc import Callable
from datetime import date, datetime, timezone
from http import HTTPStatus
from typing import Any
from uuid import UUID

import pytest
import pytest_asyncio
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from adapters.models import UserModel
from domain.entities import User
from domain.value_objects import ColorTheme, Language
from ports.security import IPasswordManager
from web.di import Di
from web.security import IJwtManager


@pytest_asyncio.fixture
async def users_collection(
    mongo_database: AsyncIOMotorDatabase,
) -> AsyncIOMotorCollection:
    return mongo_database['users']


@pytest.mark.asyncio
async def test_authenticate_user_success_CREATED(
    app_client: AsyncClient,
    users_collection: AsyncIOMotorCollection,
    subtract_years_from_today: Callable[[int], date],
    is_uuid: Callable[[Any], bool],
    as_uuid: Callable[[str], UUID],
) -> None:
    original_password: str = 'Windows#123'
    hashed_password: str = Di.get_raw(IPasswordManager).hash(original_password)

    user: User = User(
        username='Adriano Lombardi',
        birth_date=subtract_years_from_today(43),
        color_theme=ColorTheme.LIGHT,
        email='lombardi.adriano@gmail.com',
        hashed_password=hashed_password,
        language=Language.PT_BR,
    )

    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    payload: dict[str, Any] = {
        'username': user.email,
        'password': original_password,
    }

    response = await app_client.post('/auth/token/', data=payload)
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.CREATED

    assert response_data.get('token_type') == 'bearer'
    assert isinstance((token := response_data.get('access_token')), str)

    decoded_token: dict[str, str] = Di.get_raw(IJwtManager).decode_access_token(token)

    assert isinstance((exp := decoded_token.get('exp')), int)

    exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
    now = datetime.now(timezone.utc)

    assert exp_datetime > now

    assert isinstance((sub := decoded_token.get('sub')), str)
    assert is_uuid(sub)

    result: dict[str, Any] | None = await users_collection.find_one(
        {'_id': as_uuid(sub)}
    )

    assert isinstance(result, dict)
    assert result.get('email') == user.email


@pytest.mark.asyncio
async def test_when_try_to_authenticate_user_with_invalid_credentials_returns_UNAUTHORIZED(
    app_client: AsyncClient, is_datetime: Callable[[Any], bool]
) -> None:
    payload: dict[str, Any] = {
        'username': 'email@gmail.com',
        'password': 'Windows#123',
    }

    response = await app_client.post('/auth/token/', data=payload)
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.headers.get('WWW-Authenticate') == 'Bearer'

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'InvalidCredentials',
        'scope': 'AuthException',
        'kind': 'Unauthorized',
        'message': 'Email ou senha inválidos',
        'status': HTTPStatus.UNAUTHORIZED,
    }


@pytest.mark.asyncio
async def test_when_try_to_authenticate_user_with_invalid_email_returns_UNAUTHORIZED(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
    users_collection: AsyncIOMotorCollection,
    subtract_years_from_today: Callable[[int], date],
) -> None:
    original_password: str = 'Windows#123'
    hashed_password: str = Di.get_raw(IPasswordManager).hash(original_password)

    user: User = User(
        username='Adriano Lombardi',
        birth_date=subtract_years_from_today(43),
        color_theme=ColorTheme.LIGHT,
        email='lombardi.adriano@gmail.com',
        hashed_password=hashed_password,
        language=Language.PT_BR,
    )

    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    payload: dict[str, Any] = {
        'username': 'email@gmail.com',
        'password': original_password,
    }

    response = await app_client.post('/auth/token/', data=payload)
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.headers.get('WWW-Authenticate') == 'Bearer'

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'InvalidCredentials',
        'scope': 'AuthException',
        'kind': 'Unauthorized',
        'message': 'Email ou senha inválidos',
        'status': HTTPStatus.UNAUTHORIZED,
    }


@pytest.mark.asyncio
async def test_when_try_to_authenticate_user_with_invalid_password_returns_UNAUTHORIZED(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
    users_collection: AsyncIOMotorCollection,
    subtract_years_from_today: Callable[[int], date],
) -> None:
    hashed_password: str = Di.get_raw(IPasswordManager).hash('Windows#123')

    user: User = User(
        username='Adriano Lombardi',
        birth_date=subtract_years_from_today(43),
        color_theme=ColorTheme.LIGHT,
        email='lombardi.adriano@gmail.com',
        hashed_password=hashed_password,
        language=Language.PT_BR,
    )

    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    payload: dict[str, Any] = {
        'username': user.email,
        'password': 'senha@123',
    }

    response = await app_client.post('/auth/token/', data=payload)
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.headers.get('WWW-Authenticate') == 'Bearer'

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'InvalidCredentials',
        'scope': 'AuthException',
        'kind': 'Unauthorized',
        'message': 'Email ou senha inválidos',
        'status': HTTPStatus.UNAUTHORIZED,
    }


@pytest.mark.asyncio
async def test_when_try_to_authenticate_a_deactivated_user_returns_FORBIDDEN(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
    users_collection: AsyncIOMotorCollection,
    subtract_years_from_today: Callable[[int], date],
) -> None:
    original_password: str = 'Windows#123'
    hashed_password: str = Di.get_raw(IPasswordManager).hash(original_password)

    user: User = User(
        username='Adriano Lombardi',
        birth_date=subtract_years_from_today(43),
        color_theme=ColorTheme.LIGHT,
        email='lombardi.adriano@gmail.com',
        hashed_password=hashed_password,
        language=Language.PT_BR,
        is_active=False,
    )

    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    payload: dict[str, Any] = {
        'username': user.email,
        'password': original_password,
    }

    response = await app_client.post('/auth/token/', data=payload)
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.FORBIDDEN

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'UserIsDeactivated',
        'scope': 'UserException',
        'kind': 'Forbidden',
        'message': f'O usuário {user.email} está desativado',
        'status': HTTPStatus.FORBIDDEN,
    }
