from fastapi import APIRouter, Depends, HTTPException, status, Query
from uuid import UUID
from typing import List, Optional, Dict

from sqlalchemy.ext.asyncio import AsyncSession

from services.url_srv import UrlService
from schemas.url_sch import UrlCreate, UrlResponse, UrlUpdate
from schemas.response_sch import SuccessResponse as Response, ErrorResponse as Error
from dependencies.database import get_db
from fastapi.responses import JSONResponse


router = APIRouter()

@router.get("/{shortlink}", response_model=str)
async def redirect_to_original_url(
    shortlink: str,
    db: AsyncSession = Depends(get_db)
):
    """Redirect to the original URL and increment the click counter."""
    print(shortlink)
    service = UrlService(db)
    result = await service.redirect(shortlink)
    return result