import logging
from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse

from utils.authorize import check_access
from models import Url, User
from repositories import UrlRepositories
from schemas.url_sch import UrlCreate, UrlResponse, UrlUpdate
from configs.settings import settings
from utils.shortlink import Shortlink

logger = logging.getLogger(__name__)

class UrlService:
    def __init__(self, session: AsyncSession):
        self.reps = UrlRepositories(session)
        self.max_retries = 4

    async def create_shortlink(self, data: UrlCreate, user: User) -> UrlResponse:
        """Create a new shortlink for a given URL."""
        try:
            data.shortlink = await self._shortlink_handler(data.shortlink)
            result = await self.reps.create({
                "original_url": str(data.original_url),
                "shortlink": data.shortlink,
                "title": data.title,
                "user_id": user.id
            })
            logger.info(f"Created shortlink: {data.shortlink} for URL: {data.original_url}")
            return await self._build_response(result)
        except Exception as e:
            logger.error(f"Failed to create shortlink: {e}")
            raise

    async def get_all(self, skip: int = 0, limit: int = 100, filters: dict = None) -> List[UrlResponse]:
        """Retrieve a paginated list of URLs, optionally filtered."""
        try:
            result = await self.reps.get_all(skip, limit, filters)
            return [ await self._build_response(url) for url in result["items"]]
        except Exception as e:
            logger.error(f"Failed to get shortlinks: {e}")
            raise

    async def get_by_id(self, id: UUID) -> UrlResponse:
        """Get the full data of a shortlink based on the given ID."""
        try:
            result = await self.reps.get(id)
            if not result: raise LookupError('Shortlink not found') 
            return  await self._build_response(result)
        except Exception as e:
            logger.error(f"Failed to get shortlink: {e}")
            raise

    async def redirect(self, shortlink: str) -> str:
        """Redirect to the original URL and increment the click counter."""
        try:
            url = await self.reps.get_by_shortlink(shortlink)
            if not url: raise LookupError('Shortlink not found')
            url = await self.reps.increment_clicks(url) 
            return RedirectResponse(url.original_url)
        except Exception as e:
            logger.error(f"Failed to redirect: {e}")
            raise

    async def update(self, id: UUID, data: UrlUpdate) -> UrlResponse:
        """Update an existing shortlink with the given data."""
        try:
            result = await self.reps.get(id)
            if not result: raise LookupError('Shortlink not found')
            updated = await self.reps.update(id, data)
            return  await self._build_response(updated)
        except Exception as e:
            logger.error(f"Failed to update URL: {e}")
            raise

    async def delete(self, id: UUID) -> bool:
        """Delete a shortlink based on the given ID."""
        try:
            url = await self.reps.get(id)
            if not url: raise LookupError("Shortlink not found")
            await self.reps.delete(id)
            return True
        except Exception as e:
            logger.error(f"Failed to delete URL: {e}")
            raise

    async def _shortlink_handler(self, shortlink: Optional[str]) -> str:
        if shortlink is not None:
            # Check existing code
            if await self.reps.shortlink_exist(shortlink): raise ValueError("The shortlink has been used")

            # Check restricted string
            if shortlink in settings.RESTRICTED_SHORTLINK: raise ValueError("The shortlink is restricted")

        else:
            shortlink = await self._generate_shortlink()
        return shortlink

    async def _generate_shortlink(self) -> str:
        """
        Generate a unique short code.
        Returns:
            A unique short code.
        """
        while True:
            shortlink = Shortlink().generate()
            if not await self.reps.shortlink_exist(shortlink): break
        return shortlink

    async def _build_response(self, url: Url) -> UrlResponse:
        return UrlResponse(
            id=str(url.id),
            title=url.title or "",
            original_url=url.original_url,
            shortlink=url.shortlink,
            clicks=url.clicks,
            is_active=url.is_active,
            created_at=url.created_at.isoformat(),
            updated_at=url.updated_at.isoformat(),
        )
