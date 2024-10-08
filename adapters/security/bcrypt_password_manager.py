from bcrypt import checkpw, gensalt, hashpw

from ports.security import IPasswordManager


class BcryptPasswordManager(IPasswordManager):
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return checkpw(plain_password.encode(), hashed_password.encode())

    def hash(self, password: str) -> str:
        return hashpw(password.encode(), gensalt()).decode()
