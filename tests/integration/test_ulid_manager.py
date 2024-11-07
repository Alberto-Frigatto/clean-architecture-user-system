import pytest

from adapters.id import UlidManager


@pytest.fixture
def id_manager() -> UlidManager:
    return UlidManager()


def test_create_ULID_as_str_with_26_base32_chars(id_manager: UlidManager) -> None:
    ulid: str = id_manager.generate()

    assert isinstance(ulid, str)
    assert len(ulid) == 26

    base32_alphabet: str = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'

    assert all(c in base32_alphabet for c in ulid)
