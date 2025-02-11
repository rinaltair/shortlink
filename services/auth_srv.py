import logging
from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.authentication import AuthenticationError

from models import User
from repositories import UserRepositories
from utils import hash
from utils.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self,  session: AsyncSession):
        self.user_repo = UserRepositories(session)
        self.hash = hash

    async def access_token(self, user: User):
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires)
        return access_token


    async def authenticate_user(self, username: str, password: str):
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
