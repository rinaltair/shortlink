from fastapi import APIRouter, Depends, status, Query
from uuid import UUID
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.auth import auth_user
from dependencies.database import get_db
from models.user_model import User
from services.url_srv import UrlService
from schemas.url_sch import UrlCreate, UrlUpdate
from schemas.response_sch import SuccessResponse as Response


router = APIRouter()

@router.post("/", response_model=Response, status_code=status.HTTP_201_CREATED)
async def create_shortlink(
    data: UrlCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_user)
):
    """Create a new shortlink for a given URL."""
    service = UrlService(db)
    result = await service.create_shortlink(data, user)
    return Response(data=result, message="Shortlink created successfully", code=status.HTTP_201_CREATED)

@router.get("/", response_model=Response, status_code=status.HTTP_200_OK)
async def get_all_urls(
    skip: int = 0,
    limit: int = 100,
    filters: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Retrieve a paginated list of URLs, optionally filtered."""
    service = UrlService(db)
    result = await service.get_all(skip, limit, filters)
    return Response(data=result, message="Shortlinks retrieved successfully")

@router.get("/{id}", response_model=Response, status_code=status.HTTP_200_OK)
async def get_url_by_id(
    id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get the full data of a shortlink based on the given ID."""
    service = UrlService(db)
    result  = await service.get_by_id(id)
    return Response(data=result, message="Shortlink retrieved successfully")

@router.put("/{id}", response_model=Response, status_code=status.HTTP_200_OK)
async def update_url(
    id: UUID,
    data: UrlUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update an existing shortlink with the given data."""
    service = UrlService(db)
    result =  await service.update(id, data, current_user)
    return Response(data=result, message="Shortlink updated successfully")

@router.post("/delete",  status_code=status.HTTP_204_NO_CONTENT)
async def delete_url(
    id: UUID,
    db: AsyncSession = Depends(get_db),
):
    """Delete a shortlink based on the given ID."""
    service = UrlService(db)
    await service.delete(id, auth_user)
    # return Response(message="Shortlink deleted successfully")