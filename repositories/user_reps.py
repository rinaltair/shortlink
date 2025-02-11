from abc import ABC
from typing import Optional

from pydantic import EmailStr
from sqlmodel import select

from models import User
from repositories import BaseRepository
from schemas.user_sch import UserCreate, UserUpdate


class UserRepositories(BaseRepository[User, UserCreate, UserUpdate]):
    def __init__(self, session):
        self.session = session
        self.model = User

    async def get_by_username(self, username: str) -> Optional[User]:
        """
        Get User by username
        Args:
            username: The unique username
        Returns:
            User instance or None if not found
        """
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_by_email(self, email: EmailStr | str) -> Optional[User]:
        """
        Get User by email
        Args:
            email: The unique email
        Returns:
            User instance or None if not found
        """
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalars().first()
