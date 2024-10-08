import pytest

from adapters.security import BcryptPasswordManager


@pytest.fixture
def password_manager() -> BcryptPasswordManager:
    return BcryptPasswordManager()


def test_hash_password(
    password_manager: BcryptPasswordManager,
) -> None:
    password: str = 'senha@123'
    hashed_password: str = password_manager.hash(password)

    assert hashed_password != password


def test_verify_password(password_manager: BcryptPasswordManager) -> None:
    password: str = 'senha@123'
    hashed_password: str = password_manager.hash(password)

    assert hashed_password != password
    assert password_manager.verify(password, hashed_password) == True
