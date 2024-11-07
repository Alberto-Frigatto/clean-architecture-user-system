from ulid import ULID


class Ulid:
    def __init__(self, value: str | bytes | None = None) -> None:
        if isinstance(value, str):
            self._ulid: ULID = ULID.from_str(value)
        elif isinstance(value, bytes):
            self._ulid: ULID = ULID.from_bytes(value)
        elif value is None:
            self._ulid: ULID = ULID()
        else:
            raise TypeError('ULID inválido')

    def __bytes__(self) -> bytes:
        return bytes(self._ulid)

    def __str__(self) -> str:
        return str(self._ulid)
