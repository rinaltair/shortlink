import logging

from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from repositories import UserRepositories
from schemas.user_sch import UserCreate, UserResponse
from utils.password import Password

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession):
        self.reps = UserRepositories(session)
        self.max_retries = 4

    async def create_user(self, data: UserCreate):
        """Create a new User."""
        try:
            data = await self._unique_handler(data)
            data.password = Password.hash_pwd(data.password)
            result = await self.reps.create({
                "username": data.username,
                "email": data.email,
                "password_hash": data.password,
            })
            logger.info(f"Created username: {data.username} with email: {data.email}")
            return await self._build_response(result)
        except Exception as e:
            logger.error(f"Failed to create shortlink: {e}")
            raise

    async def get_all(self, skip: int = 0, limit: int = 100, filters: dict = None):
        """Retrieve a paginated list of Users, optionally filtered."""
        try:
            result = await self.reps.get_all(skip, limit, filters)
            return result
        except Exception as e:
            raise e

    async def _unique_handler(self, data: UserCreate) -> UserCreate:
        """Check if the username or email already exists in the database."""
        if await self.reps.get_by_username(data.username):
            raise ValueError('Username already exists')
        if await self.reps.get_by_email(data.email):
            raise ValueError('Email already exists')
        return data

    async def _build_response(self, user: User) -> UserResponse:
        return UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            role=user.role or 'user',
            is_active=user.is_active,
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat(),
        )
