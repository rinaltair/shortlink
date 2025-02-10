import logging
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from models import User
from repositories import UserRepositories
from schemas.user_sch import UserCreate, UserResponse
from utils.password import Password

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession):
        self.reps = UserRepositories(session)

    async def create_user(self, data: UserCreate):
        """Create a new User."""
        try:
            data.username = await self._unique_username_handler(data)
            data.email = await self._unique_email_handler(data)
            data.password = Password.hash_pwd(data.password)
            result = await self.reps.create({
                "username": data.username,
                "email": data.email,
                "password_hash": data.password,
            })
            logger.info(f"Created username: {data.username} with email: {data.email}")
            return await self._build_response(result)
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise

    async def get_all(self, skip: int = 0, limit: int = 100, filters: dict = None):
        """Retrieve a paginated list of Users, optionally filtered."""
        try:
            result = await self.reps.get_all(skip, limit, filters)
            return result
        except Exception as e:
            logger.error(f"Failed to get users: {e}")
            raise e

    async def get_by_id(self, id: UUID):
        """Get the full data of a User based on the given ID."""
        try:
            result = await self.reps.get(id)
            if not result:
                raise LookupError('User not found')
            return await self._build_response(result)
        except Exception as e:
            logger.error(f"Failed to get user: {e}")
            raise


    async def _unique_email_handler(self, email: EmailStr | str) -> str:
        """Check if the username or email already exists in the database."""
        if await self.reps.get_by_email(email):
            raise ValueError('Email already exists')
        return email

    async def _unique_username_handler(self, username: str) -> str:
        """Check if the username or email already exists in the database."""
        if await self.reps.get_by_username(username):
            raise ValueError('Username already exists')
        return username

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
