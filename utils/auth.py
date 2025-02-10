from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Auth:

    def get_hash_password(password: str) -> str:
        return pwd_context.hash(password)
