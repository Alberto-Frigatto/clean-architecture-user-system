import base64
from collections.abc import Callable

import pytest

from adapters.id import Ulid


@pytest.fixture
def base32_alphabet() -> str:
    return '0123456789ABCDEFGHJKMNPQRSTVWXYZ'


@pytest.fixture
def ulid_str_to_16_bytes(base32_alphabet: str) -> Callable[[str], bytes]:
    def ulid_str_to_16_bytes_function(ulid: str) -> bytes:
        bits: int = 0

        for char in ulid:
            bits = (bits << 5) | base32_alphabet.index(char)

        return bits.to_bytes(16, byteorder='big')

    return ulid_str_to_16_bytes_function


def test_create_ulid_from_None(base32_alphabet: str) -> None:
    ulid: Ulid = Ulid()

    assert len(str(ulid)) == 26
    assert len(bytes(ulid)) == 16

    assert all(char in base32_alphabet for char in str(ulid))


def test_create_ulid_from_str(base32_alphabet: str) -> None:
    original_str: str = '01JBCMXTNBPYER16TDN24FT857'
    ulid: Ulid = Ulid(original_str)

    assert len(str(ulid)) == 26
    assert len(bytes(ulid)) == 16
    assert str(ulid) == original_str

    assert all(char in base32_alphabet for char in str(ulid))


def test_create_ulid_from_bytes(
    base32_alphabet: str, ulid_str_to_16_bytes: Callable[[str], bytes]
) -> None:
    original_str: str = '01JBCMXTNBPYER16TDN24FT857'
    original_bytes: bytes = ulid_str_to_16_bytes(original_str)

    ulid: Ulid = Ulid(original_bytes)

    assert len(str(ulid)) == 26
    assert len(bytes(ulid)) == 16
    assert bytes(ulid) == original_bytes
    assert str(ulid) == original_str

    assert all(char in base32_alphabet for char in str(ulid))


def test_when_try_to_create_ulid_from_bytes_without_16_bytes_raises_ValueError() -> (
    None
):
    with pytest.raises(ValueError):
        Ulid('01JBCMXTNBPYER16TDN24FT857'.encode())


def test_when_try_to_create_ulid_from_dict_raises_TypeError() -> None:
    with pytest.raises(TypeError):
        Ulid({})  # type: ignore
