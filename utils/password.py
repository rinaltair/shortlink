from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Password:
    def __init__(self, password: str):
        self.password = password

    def hash_pwd(password: str) -> str:
        return pwd_context.hash(password)
