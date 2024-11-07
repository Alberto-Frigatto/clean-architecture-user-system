from collections.abc import Callable
from datetime import date, datetime, timedelta, timezone
from http import HTTPStatus
from typing import Any

import jwt
import pytest
import pytest_asyncio
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from adapters.models import UserModel
from domain.entities import User
from domain.value_objects import ColorTheme, Language
from ports.id import IIdManager
from ports.security import IPasswordManager
from web.config.settings.base import Settings
from web.di import Di
from web.security import IJwtManager


@pytest_asyncio.fixture
async def users_collection(
    mongo_database: AsyncIOMotorDatabase,
) -> AsyncIOMotorCollection:
    return mongo_database['users']


@pytest.fixture
def user(subtract_years_from_today: Callable[[int], date]) -> User:
    original_password: str = 'Windows#123'
    hashed_password: str = Di.get_raw(IPasswordManager).hash(original_password)

    id_manager: IIdManager = Di.get_raw(IIdManager)

    return User(
        id=id_manager.generate(),
        username='Adriano Lombardi',
        birth_date=subtract_years_from_today(43),
        color_theme=ColorTheme.LIGHT,
        email='lombardi.adriano@gmail.com',
        hashed_password=hashed_password,
        language=Language.PT_BR,
    )


@pytest.mark.asyncio
async def test_create_user_success_CREATED(
    app_client: AsyncClient,
    users_collection: AsyncIOMotorCollection,
    is_ulid: Callable[[Any], bool],
    from_ulid_to_bytes: Callable[[str], bytes],
    is_datetime: Callable[[Any], bool],
    normalize_datetime: Callable[[datetime], datetime],
    subtract_years_from_today: Callable[[int], date],
) -> None:
    payload: dict[str, Any] = {
        'username': 'Gustavo Lopes da Silva',
        'email': 'gustavo.lopes@outlook.com.br',
        'password': 'Windows#123',
        'birth_date': subtract_years_from_today(18).strftime('%Y-%m-%d'),
        'color_theme': ColorTheme.DARK.value,
        'language': Language.EN_UK.value,
    }

    response = await app_client.post('/users/', json=payload)
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.CREATED

    assert is_ulid(response_data.get('id'))
    created_user_id: bytes = from_ulid_to_bytes(response_data.pop('id'))

    assert is_datetime(response_data.get('created_at'))
    created_user_created_at = response_data.pop('created_at')

    assert response_data == {
        'birth_date': payload['birth_date'],
        'color_theme': payload['color_theme'],
        'email': payload['email'],
        'is_active': True,
        'language': payload['language'],
        'username': payload['username'],
    }

    created_user_document: dict[str, Any] | None = await users_collection.find_one(
        {'_id': created_user_id}
    )

    assert created_user_document is not None

    created_user: User = UserModel.from_document(created_user_document).to_entity()

    assert from_ulid_to_bytes(created_user.id) == created_user_id
    assert created_user.birth_date == date.fromisoformat(payload['birth_date'])
    assert created_user.color_theme == response_data['color_theme']
    assert normalize_datetime(created_user.created_at) == normalize_datetime(
        datetime.fromisoformat(created_user_created_at)
    )
    assert created_user.email == response_data['email']
    assert created_user.color_theme == response_data['color_theme']
    assert created_user.hashed_password != payload['password']
    assert created_user.is_active == response_data['is_active']
    assert created_user.language == response_data['language']


@pytest.mark.asyncio
async def test_when_try_to_create_an_user_with_email_from_existing_user_returns_CONFLICT(
    app_client: AsyncClient,
    users_collection: AsyncIOMotorCollection,
    subtract_years_from_today: Callable[[int], date],
    is_datetime: Callable[[Any], bool],
    user: User,
) -> None:
    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    payload: dict[str, Any] = {
        'username': 'Adriano Lombardi',
        'email': user.email,
        'password': 'Windows#123',
        'birth_date': subtract_years_from_today(43).strftime('%Y-%m-%d'),
        'color_theme': ColorTheme.DARK.value,
        'language': Language.PT_BR.value,
    }

    response = await app_client.post('/users/', json=payload)
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.CONFLICT

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'UserAlreadyExists',
        'scope': 'UserException',
        'type': 'Conflict',
        'message': f'The user {user.email} already exists',
        'status': HTTPStatus.CONFLICT,
    }


@pytest.mark.asyncio
async def test_when_try_to_create_an_underage_user_returns_UNPROCESSABLE_ENTITY(
    app_client: AsyncClient,
    subtract_years_from_today: Callable[[int], date],
    is_datetime: Callable[[Any], bool],
) -> None:
    payload: dict[str, Any] = {
        'username': 'Adriano Lombardi',
        'email': 'adriano@hotmail.com',
        'password': 'Windows#123',
        'birth_date': subtract_years_from_today(17).strftime('%Y-%m-%d'),
        'color_theme': ColorTheme.DARK.value,
        'language': Language.PT_BR.value,
    }

    response = await app_client.post('/users/', json=payload)
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'UserIsUnderage',
        'scope': 'UserException',
        'type': 'UnprocessableEntity',
        'message': 'The user is underage',
        'status': HTTPStatus.UNPROCESSABLE_ENTITY,
    }


@pytest.mark.asyncio
async def test_when_try_to_create_an_user_with_invalid_data_returns_BAD_RESQUEST(
    app_client: AsyncClient,
    subtract_years_from_today: Callable[[int], date],
    is_datetime: Callable[[Any], bool],
) -> None:
    payload: dict[str, Any] = {
        'username': 'Nome 123 # ',
        'email': 'adriano',
        'password': 'abcdefghijkl',
        'birth_date': subtract_years_from_today(101).strftime('%Y-%m-%d'),
        'color_theme': 'abc',
        'language': 'abc',
    }

    response = await app_client.post('/users/', json=payload)
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'InvalidDataSent',
        'scope': 'ApiValidationException',
        'type': 'BadRequest',
        'message': 'Invalid data sent',
        'detail': [
            {
                'input': payload['username'],
                'loc': [
                    'body',
                    'username',
                ],
                'message': "String should match pattern '^[a-zA-ZÀ-ÿç\\s]+$'",
                'type': 'string_pattern_mismatch',
            },
            {
                'input': payload['email'],
                'loc': [
                    'body',
                    'email',
                ],
                'message': 'value is not a valid email address: An email address must have an @-sign.',
                'type': 'value_error',
            },
            {
                'input': payload['password'],
                'loc': [
                    'body',
                    'password',
                ],
                'message': 'Value error, Password doesn\'t have the required characters',
                'type': 'value_error',
            },
            {
                'input': payload['birth_date'],
                'loc': [
                    'body',
                    'birth_date',
                ],
                'message': 'Value error, Invalid birth date',
                'type': 'value_error',
            },
            {
                'input': payload['color_theme'],
                'loc': [
                    'body',
                    'color_theme',
                ],
                'message': "Input should be 'light' or 'dark'",
                'type': 'enum',
            },
            {
                'input': payload['language'],
                'loc': [
                    'body',
                    'language',
                ],
                'message': "Input should be 'en_us', 'en_uk', 'pt_br', 'pt_pt', 'es_es', "
                "'fr_fr', 'de_de', 'ja_jp', 'zh_cn' or 'ru_ru'",
                'type': 'enum',
            },
        ],
        'status': HTTPStatus.BAD_REQUEST,
    }


@pytest.mark.asyncio
async def test_get_user_info_success_OK(
    app_client: AsyncClient,
    users_collection: AsyncIOMotorCollection,
    is_datetime: Callable[[Any], bool],
    authorization_header: Callable[[str], dict[str, str]],
    user: User,
) -> None:
    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    jwt_token: str = Di.get_raw(IJwtManager).create_access_token(str(user.id))

    response = await app_client.get(
        '/users/me', headers=authorization_header(jwt_token)
    )
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.OK

    assert is_datetime(response_data.pop('created_at'))

    assert response_data == {
        'id': str(user.id),
        'birth_date': user.birth_date.strftime('%Y-%m-%d'),
        'color_theme': user.color_theme,
        'email': user.email,
        'is_active': user.is_active,
        'language': user.language,
        'username': user.username,
    }


@pytest.mark.asyncio
async def test_when_try_to_get_user_info_without_jwt_token_returns_UNAUTHORIZED(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
) -> None:
    response = await app_client.get('/users/me')
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.headers.get('WWW-Authenticate') == 'Bearer'

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'MissingJwt',
        'scope': 'ApiSecurityException',
        'type': 'Unauthorized',
        'message': 'JWT token not provided',
        'status': HTTPStatus.UNAUTHORIZED,
    }


@pytest.mark.asyncio
async def test_when_try_to_get_user_info_with_jwt_token_with_non_existent_uuid_returns_UNAUTHORIZED(
    app_client: AsyncClient,
    users_collection: AsyncIOMotorCollection,
    is_datetime: Callable[[Any], bool],
    authorization_header: Callable[[str], dict[str, str]],
    user: User,
) -> None:
    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    non_existent_id: str = Di.get_raw(IIdManager).generate()
    jwt_token: str = Di.get_raw(IJwtManager).create_access_token(non_existent_id)

    response = await app_client.get(
        '/users/me', headers=authorization_header(jwt_token)
    )
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.headers.get('WWW-Authenticate') == 'Bearer'

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'UserNotFound',
        'scope': 'UserException',
        'type': 'Unauthorized',
        'message': f'The user {non_existent_id} wasn\'t found',
        'status': HTTPStatus.UNAUTHORIZED,
    }


@pytest.mark.asyncio
async def test_when_try_to_get_user_info_with_jwt_token_with_invalid_sub_returns_UNAUTHORIZED(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
    authorization_header: Callable[[str], dict[str, str]],
) -> None:
    jwt_token: str = Di.get_raw(IJwtManager).create_access_token('abc')

    response = await app_client.get(
        '/users/me', headers=authorization_header(jwt_token)
    )
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.headers.get('WWW-Authenticate') == 'Bearer'

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'InvalidJwt',
        'scope': 'ApiSecurityException',
        'type': 'Unauthorized',
        'message': 'Invalid JWT token',
        'status': HTTPStatus.UNAUTHORIZED,
    }


@pytest.mark.asyncio
async def test_when_try_to_get_user_info_from_deactivated_user_returns_FORBIDDEN(
    app_client: AsyncClient,
    users_collection: AsyncIOMotorCollection,
    is_datetime: Callable[[Any], bool],
    authorization_header: Callable[[str], dict[str, str]],
    subtract_years_from_today: Callable[[int], date],
) -> None:
    id_manager: IIdManager = Di.get_raw(IIdManager)

    user: User = User(
        id=id_manager.generate(),
        username='Adriano Lombardi',
        birth_date=subtract_years_from_today(43),
        color_theme=ColorTheme.LIGHT,
        email='lombardi.adriano@gmail.com',
        hashed_password='senha',
        language=Language.PT_BR,
        is_active=False,
    )

    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    jwt_token: str = Di.get_raw(IJwtManager).create_access_token(str(user.id))

    response = await app_client.get(
        '/users/me', headers=authorization_header(jwt_token)
    )
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.FORBIDDEN

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'UserIsDeactivated',
        'scope': 'UserException',
        'type': 'Forbidden',
        'message': f'The user {user.email} is deactivated',
        'status': HTTPStatus.FORBIDDEN,
    }


@pytest.mark.asyncio
async def test_when_try_to_get_user_info_with_expired_jwt_token_returns_UNAUTHORIZED(
    app_client: AsyncClient,
    users_collection: AsyncIOMotorCollection,
    is_datetime: Callable[[Any], bool],
    authorization_header: Callable[[str], dict[str, str]],
    user: User,
) -> None:
    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    settings: Settings = Di.get_raw(Settings)
    jwt_token: str = jwt.encode(
        {
            'sub': str(user.id),
            'exp': datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        settings.secret_key,
        algorithm=settings.jwt_algorithm,
    )

    response = await app_client.get(
        '/users/me', headers=authorization_header(jwt_token)
    )
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.headers.get('WWW-Authenticate') == 'Bearer'

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'ExpiredJwt',
        'scope': 'ApiSecurityException',
        'type': 'Unauthorized',
        'message': 'Expired JWT token',
        'status': HTTPStatus.UNAUTHORIZED,
    }


@pytest.mark.asyncio
async def test_deactivate_user_success_NO_CONTENT(
    app_client: AsyncClient,
    users_collection: AsyncIOMotorCollection,
    authorization_header: Callable[[str], dict[str, str]],
    from_ulid_to_bytes: Callable[[str], bytes],
    user: User,
) -> None:
    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    jwt_token: str = Di.get_raw(IJwtManager).create_access_token(str(user.id))

    response = await app_client.patch(
        '/users/me/deactivate', headers=authorization_header(jwt_token)
    )

    assert response.status_code == HTTPStatus.NO_CONTENT

    assert not response.content

    deactivated_user_document: dict[str, Any] | None = await users_collection.find_one(
        {'_id': from_ulid_to_bytes(user.id)}
    )

    assert deactivated_user_document is not None

    deactivated_user: User = UserModel.from_document(
        deactivated_user_document
    ).to_entity()

    assert deactivated_user.is_active == False


@pytest.mark.asyncio
async def test_when_try_to_deactivate_user_without_jwt_token_returns_UNAUTHORIZED(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
) -> None:
    response = await app_client.patch('/users/me/deactivate')
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.headers.get('WWW-Authenticate') == 'Bearer'

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'MissingJwt',
        'scope': 'ApiSecurityException',
        'type': 'Unauthorized',
        'message': 'JWT token not provided',
        'status': HTTPStatus.UNAUTHORIZED,
    }


@pytest.mark.asyncio
async def test_update_user_preferences_success_OK(
    app_client: AsyncClient,
    users_collection: AsyncIOMotorCollection,
    from_ulid_to_bytes: Callable[[str], bytes],
    authorization_header: Callable[[str], dict[str, str]],
    is_datetime: Callable[[Any], bool],
    user: User,
) -> None:
    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    payload: dict[str, Any] = {
        'color_theme': ColorTheme.DARK,
        'language': Language.FR_FR,
    }

    jwt_token: str = Di.get_raw(IJwtManager).create_access_token(str(user.id))

    response = await app_client.patch(
        '/users/me/preferences',
        headers=authorization_header(jwt_token),
        json=payload,
    )
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.OK

    assert is_datetime(response_data.pop('created_at'))

    assert response_data == {
        'id': str(user.id),
        'birth_date': user.birth_date.strftime('%Y-%m-%d'),
        'color_theme': payload['color_theme'],
        'email': user.email,
        'is_active': user.is_active,
        'language': payload['language'],
        'username': user.username,
    }

    updated_user_document: dict[str, Any] | None = await users_collection.find_one(
        {'_id': from_ulid_to_bytes(user.id)}
    )

    assert updated_user_document is not None

    updated_user: User = UserModel.from_document(updated_user_document).to_entity()

    assert updated_user.color_theme == payload['color_theme']
    assert updated_user.language == payload['language']


@pytest.mark.asyncio
async def test_when_try_to_update_user_preferences_without_jwt_token_returns_UNAUTHORIZED(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
) -> None:
    payload: dict[str, Any] = {
        'color_theme': ColorTheme.DARK,
        'language': Language.FR_FR,
    }

    response = await app_client.patch('/users/me/preferences', json=payload)
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.headers.get('WWW-Authenticate') == 'Bearer'

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'MissingJwt',
        'scope': 'ApiSecurityException',
        'type': 'Unauthorized',
        'message': 'JWT token not provided',
        'status': HTTPStatus.UNAUTHORIZED,
    }


@pytest.mark.asyncio
async def test_update_user_personal_data_success_OK(
    app_client: AsyncClient,
    users_collection: AsyncIOMotorCollection,
    subtract_years_from_today: Callable[[int], date],
    authorization_header: Callable[[str], dict[str, str]],
    from_ulid_to_bytes: Callable[[str], bytes],
    is_datetime: Callable[[Any], bool],
    user: User,
) -> None:
    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    payload: dict[str, str] = {
        'birth_date': subtract_years_from_today(22).strftime('%Y-%m-%d'),
        'email': 'adriano@outlook.com',
        'username': 'Adriano da Silva',
    }

    jwt_token: str = Di.get_raw(IJwtManager).create_access_token(str(user.id))

    response = await app_client.patch(
        '/users/me',
        headers=authorization_header(jwt_token),
        json=payload,
    )
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.OK

    assert is_datetime(response_data.pop('created_at'))

    assert response_data == {
        'id': str(user.id),
        'birth_date': payload['birth_date'],
        'color_theme': user.color_theme,
        'email': payload['email'],
        'is_active': user.is_active,
        'language': user.language,
        'username': payload['username'],
    }

    updated_user_document: dict[str, Any] | None = await users_collection.find_one(
        {'_id': from_ulid_to_bytes(user.id)}
    )

    assert updated_user_document is not None

    updated_user: User = UserModel.from_document(updated_user_document).to_entity()

    assert updated_user.birth_date == date.fromisoformat(payload['birth_date'])
    assert updated_user.email == payload['email']
    assert updated_user.username == payload['username']


@pytest.mark.asyncio
async def test_when_try_to_update_user_personal_data_without_jwt_token_returns_UNAUTHORIZED(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
    subtract_years_from_today: Callable[[int], date],
) -> None:
    payload: dict[str, str] = {
        'birth_date': subtract_years_from_today(22).strftime('%Y-%m-%d'),
        'email': 'adriano@outlook.com',
        'username': 'Adriano da Silva',
    }

    response = await app_client.patch('/users/me', json=payload)
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.headers.get('WWW-Authenticate') == 'Bearer'

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'MissingJwt',
        'scope': 'ApiSecurityException',
        'type': 'Unauthorized',
        'message': 'JWT token not provided',
        'status': HTTPStatus.UNAUTHORIZED,
    }


@pytest.mark.asyncio
async def test_when_try_to_update_user_personal_data_with_invalid_data_returns_BAD_REQUEST(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
    subtract_years_from_today: Callable[[int], date],
    authorization_header: Callable[[str], dict[str, str]],
    users_collection: AsyncIOMotorCollection,
    user: User,
) -> None:
    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    payload: dict[str, str] = {
        'birth_date': subtract_years_from_today(101).strftime('%Y-%m-%d'),
        'email': 'adriano@.com',
        'username': 'Adriano da Silva 69',
    }

    jwt_token: str = Di.get_raw(IJwtManager).create_access_token(str(user.id))

    response = await app_client.patch(
        '/users/me',
        headers=authorization_header(jwt_token),
        json=payload,
    )
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'InvalidDataSent',
        'scope': 'ApiValidationException',
        'type': 'BadRequest',
        'message': 'Invalid data sent',
        'status': HTTPStatus.BAD_REQUEST,
        'detail': [
            {
                'input': 'Adriano da Silva 69',
                'loc': [
                    'body',
                    'username',
                ],
                'message': "String should match pattern '^[a-zA-ZÀ-ÿç\\s]+$'",
                'type': 'string_pattern_mismatch',
            },
            {
                'input': 'adriano@.com',
                'loc': [
                    'body',
                    'email',
                ],
                'message': 'value is not a valid email address: An email address cannot have '
                'a period immediately after the @-sign.',
                'type': 'value_error',
            },
            {
                'input': payload['birth_date'],
                'loc': [
                    'body',
                    'birth_date',
                ],
                'message': 'Value error, Invalid birth date',
                'type': 'value_error',
            },
        ],
    }


@pytest.mark.asyncio
async def test_when_try_to_update_user_personal_data_with_underage_birth_date_returns_UNPROCESSABLE_ENTITY(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
    authorization_header: Callable[[str], dict[str, str]],
    users_collection: AsyncIOMotorCollection,
    user: User,
) -> None:
    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    payload: dict[str, str] = {
        'birth_date': date.today().strftime('%Y-%m-%d'),
        'email': 'adriano@gmail.com',
        'username': 'Adriano da Silva',
    }

    jwt_token: str = Di.get_raw(IJwtManager).create_access_token(str(user.id))

    response = await app_client.patch(
        '/users/me',
        headers=authorization_header(jwt_token),
        json=payload,
    )
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'UserIsUnderage',
        'scope': 'UserException',
        'type': 'UnprocessableEntity',
        'message': 'The user is underage',
        'status': HTTPStatus.UNPROCESSABLE_ENTITY,
    }


@pytest.mark.asyncio
async def test_update_user_password_success_OK(
    app_client: AsyncClient,
    users_collection: AsyncIOMotorCollection,
    authorization_header: Callable[[str], dict[str, str]],
    is_datetime: Callable[[Any], bool],
    from_ulid_to_bytes: Callable[[str], bytes],
    user: User,
) -> None:
    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    payload: dict[str, str] = {
        'old_password': 'Windows#123',
        'new_password': 'Linux@2005',
        'confirm_new_password': 'Linux@2005',
    }

    jwt_token: str = Di.get_raw(IJwtManager).create_access_token(str(user.id))

    response = await app_client.patch(
        '/users/me/password',
        headers=authorization_header(jwt_token),
        json=payload,
    )
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.OK

    assert is_datetime(response_data.pop('created_at'))

    assert response_data == {
        'id': str(user.id),
        'birth_date': user.birth_date.strftime('%Y-%m-%d'),
        'color_theme': user.color_theme,
        'email': user.email,
        'is_active': user.is_active,
        'language': user.language,
        'username': user.username,
    }

    updated_user_document: dict[str, Any] | None = await users_collection.find_one(
        {'_id': from_ulid_to_bytes(user.id)}
    )

    assert updated_user_document is not None

    updated_user: User = UserModel.from_document(updated_user_document).to_entity()

    assert Di.get_raw(IPasswordManager).verify(
        payload['new_password'], updated_user.hashed_password
    )


@pytest.mark.asyncio
async def test_when_try_to_update_user_password_without_jwt_token_returns_UNAUTHORIZED(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
) -> None:
    payload: dict[str, str] = {
        'old_password': 'Windows#123',
        'new_password': 'Linux@2005',
        'confirm_new_password': 'Linux@2005',
    }

    response = await app_client.patch('/users/me/password', json=payload)
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.headers.get('WWW-Authenticate') == 'Bearer'

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'MissingJwt',
        'scope': 'ApiSecurityException',
        'type': 'Unauthorized',
        'message': 'JWT token not provided',
        'status': HTTPStatus.UNAUTHORIZED,
    }


@pytest.mark.asyncio
async def test_when_try_to_update_user_password_with_invalid_data_returns_BAD_REQUEST(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
    authorization_header: Callable[[str], dict[str, str]],
    users_collection: AsyncIOMotorCollection,
    user: User,
) -> None:
    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    payload: dict[str, str] = {
        'old_password': 'abc',
        'new_password': 'abc',
        'confirm_new_password': 'Linux2005',
    }

    jwt_token: str = Di.get_raw(IJwtManager).create_access_token(str(user.id))

    response = await app_client.patch(
        '/users/me/password',
        headers=authorization_header(jwt_token),
        json=payload,
    )
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'InvalidDataSent',
        'scope': 'ApiValidationException',
        'type': 'BadRequest',
        'message': 'Invalid data sent',
        'status': HTTPStatus.BAD_REQUEST,
        'detail': [
            {
                'type': 'string_too_short',
                'loc': ['body', 'old_password'],
                'input': 'abc',
                'message': 'String should have at least 8 characters',
            },
            {
                'type': 'string_too_short',
                'loc': ['body', 'new_password'],
                'input': 'abc',
                'message': 'String should have at least 8 characters',
            },
            {
                'type': 'value_error',
                'loc': ['body', 'confirm_new_password'],
                'input': 'Linux2005',
                'message': 'Value error, Password doesn\'t have the required characters',
            },
        ],
    }


@pytest.mark.asyncio
async def test_when_try_to_update_user_password_with_old_password_field_that_doesnt_match_the_real_one_returns_FORBIDDEN(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
    authorization_header: Callable[[str], dict[str, str]],
    users_collection: AsyncIOMotorCollection,
    user: User,
) -> None:
    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    payload: dict[str, str] = {
        'old_password': 'NaoExiste#4123',
        'new_password': 'Linux@2005',
        'confirm_new_password': 'Linux@2005',
    }

    jwt_token: str = Di.get_raw(IJwtManager).create_access_token(str(user.id))

    response = await app_client.patch(
        '/users/me/password',
        headers=authorization_header(jwt_token),
        json=payload,
    )
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.FORBIDDEN

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'OldPasswordDoesntMatch',
        'scope': 'UserException',
        'type': 'Forbidden',
        'message': 'The old password provided does not match the real one',
        'status': HTTPStatus.FORBIDDEN,
    }


@pytest.mark.asyncio
async def test_when_try_to_update_user_password_with_new_password_and_confirm_new_password_fields_that_dont_match_returns_BAD_REQUEST(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
    authorization_header: Callable[[str], dict[str, str]],
    users_collection: AsyncIOMotorCollection,
    user: User,
) -> None:
    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    payload: dict[str, str] = {
        'old_password': 'Windows#123',
        'new_password': 'Linux@2005',
        'confirm_new_password': 'Linux@2004',
    }

    jwt_token: str = Di.get_raw(IJwtManager).create_access_token(str(user.id))

    response = await app_client.patch(
        '/users/me/password',
        headers=authorization_header(jwt_token),
        json=payload,
    )
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'NewPasswordConfirmationMismatch',
        'scope': 'UserException',
        'type': 'BadRequest',
        'message': 'New password confirmation doesn\'t match the password provided',
        'status': HTTPStatus.BAD_REQUEST,
    }


@pytest.mark.asyncio
async def test_when_try_to_update_user_password_with_new_password_equals_to_old_one_returns_BAD_REQUEST(
    app_client: AsyncClient,
    is_datetime: Callable[[Any], bool],
    authorization_header: Callable[[str], dict[str, str]],
    users_collection: AsyncIOMotorCollection,
    user: User,
) -> None:
    await users_collection.insert_one(UserModel.from_entity(user).to_document())

    payload: dict[str, str] = {
        'old_password': 'Windows#123',
        'new_password': 'Windows#123',
        'confirm_new_password': 'Windows#123',
    }

    jwt_token: str = Di.get_raw(IJwtManager).create_access_token(str(user.id))

    response = await app_client.patch(
        '/users/me/password',
        headers=authorization_header(jwt_token),
        json=payload,
    )
    response_data: dict[str, Any] = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST

    assert is_datetime(response_data.pop('timestamp'))

    assert response_data == {
        'name': 'NewPasswordCantBeSameAsOld',
        'scope': 'UserException',
        'type': 'BadRequest',
        'message': f'The user\'s new password {user.email} can\'t be the same as the old one',
        'status': HTTPStatus.BAD_REQUEST,
    }
