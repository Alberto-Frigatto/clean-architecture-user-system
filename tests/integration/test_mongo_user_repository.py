from collections.abc import AsyncGenerator, Callable
from datetime import date, datetime

import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase

from adapters.repositories.user import MongoUserRepository
from domain.entities import User
from domain.value_objects import ColorTheme, Language


@pytest_asyncio.fixture
async def repository(
    motor_database: AsyncIOMotorDatabase,
) -> AsyncGenerator[MongoUserRepository]:
    yield MongoUserRepository(motor_database)


@pytest.fixture
def user() -> User:
    return User(
        username='Alberto Frigatto',
        email='alberto@gmail.com',
        hashed_password='senha_criptografada',
        birth_date=date(year=2005, month=2, day=27),
        color_theme=ColorTheme.DARK,
        language=Language.PT_BR,
    )


@pytest.mark.asyncio
async def test_create_user_success(
    repository: MongoUserRepository,
    motor_database: AsyncIOMotorDatabase,
    user: User,
    normalize_datetime: Callable[[datetime], datetime],
) -> None:
    await repository.create(user)

    created_user = await motor_database.users.find_one({'_id': user.id})

    assert created_user is not None
    assert isinstance(created_user, dict)
    assert created_user.get('_id') == user.id
    assert created_user.get('username') == user.username
    assert created_user.get('email') == user.email
    assert created_user.get('hashed_password') == user.hashed_password
    assert created_user.get('birth_date') == datetime(
        year=user.birth_date.year,
        month=user.birth_date.month,
        day=user.birth_date.day,
    )
    assert created_user.get('color_theme') == user.color_theme
    assert created_user.get('language') == user.language
    assert created_user.get('is_active') == user.is_active

    created_at: datetime | None = created_user.get('created_at')
    assert created_at is not None
    assert normalize_datetime(created_at) == normalize_datetime(user.created_at)


@pytest.mark.asyncio
async def test_get_user_by_email_success(
    repository: MongoUserRepository,
    user: User,
    normalize_datetime: Callable[[datetime], datetime],
) -> None:
    await repository.create(user)

    recupered_user: User | None = await repository.get_by_email(user.email)

    assert recupered_user is not None
    assert recupered_user.birth_date == user.birth_date
    assert recupered_user.email == user.email
    assert recupered_user.hashed_password == user.hashed_password
    assert recupered_user.is_active
    assert recupered_user.username == user.username
    assert recupered_user.color_theme == user.color_theme
    assert recupered_user.language == user.language
    assert recupered_user.id == user.id
    assert normalize_datetime(recupered_user.created_at) == normalize_datetime(
        user.created_at
    )


@pytest.mark.asyncio
async def test_when_try_to_get_an_inexistent_user_by_email_returns_None(
    repository: MongoUserRepository,
    user: User,
) -> None:
    recupered_user: User | None = await repository.get_by_email(user.email)

    assert recupered_user is None


@pytest.mark.asyncio
async def test_get_user_by_id_success(
    repository: MongoUserRepository,
    user: User,
    normalize_datetime: Callable[[datetime], datetime],
) -> None:
    await repository.create(user)

    recupered_user: User | None = await repository.get_by_id(user.id)

    assert recupered_user is not None
    assert recupered_user.birth_date == user.birth_date
    assert recupered_user.email == user.email
    assert recupered_user.hashed_password == user.hashed_password
    assert recupered_user.is_active
    assert recupered_user.username == user.username
    assert recupered_user.color_theme == user.color_theme
    assert recupered_user.language == user.language
    assert recupered_user.id == user.id
    assert normalize_datetime(recupered_user.created_at) == normalize_datetime(
        user.created_at
    )


@pytest.mark.asyncio
async def test_when_try_to_get_an_inexistent_user_by_id_returns_None(
    repository: MongoUserRepository,
    user: User,
) -> None:
    recupered_user: User | None = await repository.get_by_id(user.id)

    assert recupered_user is None


@pytest.mark.asyncio
async def test_update_user_success(
    repository: MongoUserRepository,
    motor_database: AsyncIOMotorDatabase,
    user: User,
    normalize_datetime: Callable[[datetime], datetime],
) -> None:
    await repository.create(user)

    new_user: User = User(
        id=user.id,
        username='Leandro Nogueira',
        email='leandro@hotmail.com.br',
        hashed_password='senha_criptografada_2',
        birth_date=date(year=1984, month=6, day=12),
        color_theme=ColorTheme.LIGHT,
        language=Language.PT_PT,
    )

    await repository.update(new_user)

    updated_user = await motor_database.users.find_one({'_id': new_user.id})

    assert updated_user is not None
    assert isinstance(updated_user, dict)
    assert updated_user.get('_id') == new_user.id == user.id
    assert updated_user.get('username') == new_user.username
    assert updated_user.get('email') == new_user.email
    assert updated_user.get('hashed_password') == new_user.hashed_password
    assert updated_user.get('birth_date') == datetime(
        year=new_user.birth_date.year,
        month=new_user.birth_date.month,
        day=new_user.birth_date.day,
    )
    assert updated_user.get('color_theme') == new_user.color_theme
    assert updated_user.get('language') == new_user.language
    assert updated_user.get('is_active') == new_user.is_active

    created_at: datetime | None = updated_user.get('created_at')
    assert created_at is not None
    assert normalize_datetime(created_at) == normalize_datetime(new_user.created_at)
