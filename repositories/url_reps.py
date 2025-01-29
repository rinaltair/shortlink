from typing import Optional

from sqlmodel import select

from models import Url
from repositories import BaseRepository
from schemas.url_sch import UrlCreate, UrlUpdate
from utils.shortlink import Shortlink


class UrlRepositories(BaseRepository[Url, UrlCreate, UrlUpdate]):
    def __init__(self, session):
        self.session = session

    async def shortlink_exist(self, shortlink: str) -> bool:
        """
        Check if a shortlink exists in the database.
        Args:
            shortlink: The shortlink to check for existence.
        Returns:
            True if the shortlink exists, False otherwise.
        """
        query = select(Url).where(Url.shortlink == shortlink)
        result = await self.session.execute(query)
        return result.scalars().first() is not None



    async def get_by_shortlink(self, shortlink: str) -> Optional[Url]:
        """
        Get URL by short code
        Args:
            shortlink: The unique short identifier
        Returns:
            Url instance or None if not found
        """
        result = await self.session.execute(
            select(Url).where(Url.shortlink == shortlink)
        )
        return result.scalars().first()

    async def increment_clicks(self, url: Url) -> Optional[Url]:
        """
        Atomic click counter increment
        Args:
            shortlink: The short identifier to update
        Returns:
            Updated Url instance or None if not found
        """
        if url:
            url.clicks += 1
            self.session.add(url)
            await self.session.commit()
            await self.session.refresh(url)
        return url
