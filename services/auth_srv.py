import logging
from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.authentication import AuthenticationError

from models import User
from repositories import UserRepositories
from utils import hash
from utils.jwtmanager import JWTManager as jwt
from configs.settings import settings


logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self,  session: AsyncSession):
        self.user_repo = UserRepositories(session)
        self.access_token_expire = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self.hash = hash

    async def access_token(self, user: User):
        """Generate an access token for a given user."""
        access_token_expires = timedelta(minutes=self.access_token_expire)
        access_token = await jwt().create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires)
        return access_token

    async def authenticate_user(self, username: str, password: str):
        """Authenticate a user by their username and password. """
        try:
            user = await self.user_repo.get_by_username(username)
            if user is None:
                raise AuthenticationError('User not found')
            if not self.hash.verify_password(password, user.password_hash):
                raise AuthenticationError('Invalid password')
            return user
        except Exception as e:
            logger.error(f"Unable to authenticate the user: {e}")
            raise
