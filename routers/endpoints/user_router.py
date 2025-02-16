from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Query, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.database import get_db
from models import User
from schemas.response_sch import SuccessResponse as Response
from schemas.user_sch import UserCreate, UserResponse
from services.user_srv import UserService
from utils.jwt import get_current_active_user

router = APIRouter()


@router.post("/", response_model=Response, status_code=status.HTTP_201_CREATED)
async def create_user(
        data: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    """Create a new User."""
    service = UserService(db)
    result = await service.create_user(data)
    return Response(data=result, message="User created successfully")


@router.get("/", response_model=Response, status_code=status.HTTP_200_OK)
async def get_all_users(
        skip: int = 0,
        limit: int = 100,
        filters: Optional[str] = Query(None),
        db: AsyncSession = Depends(get_db)
):
    """Retrieve a paginated list of Users, optionally filtered."""
    service = UserService(db)
    result = await service.get_all(skip, limit, filters)
    return Response(data=result, message="Users retrieved successfully")


@router.get("/{id}", response_model=Response, status_code=status.HTTP_200_OK)
async def get_user_by_id(
        id: UUID,
        db: AsyncSession = Depends(get_db),
):
    """Get the full data of a User based on the given ID."""
    service = UserService(db)
    result = await service.get_by_id(id)
    return Response(data=result, message="User retrieved successfully")


# TODO : Test the user/me for jwt token
@router.get("/users/me/", response_model=UserResponse)
async def read_users_me(
        current_user: User = Depends(get_current_active_user),
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
        current_user: User = Depends(get_current_active_user),
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.post("/{id}", response_model=Response, status_code=status.HTTP_200_OK)
async def update_user(
        id: UUID,
        data: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    # TO DO : VALIDATION WONT WORK
    """Update an existing User with the given data."""
    service = UserService(db)
    result = await service.update_user(id, data)
    return Response(data=result, message="User updated successfully")


@router.post("/{id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_url(
        id: UUID,
        db: AsyncSession = Depends(get_db)
):
    """Delete a shortlink based on the given ID."""
    service = UserService(db)
    await service.delete_user(id)
    # return Response(message="Shortlink deleted successfully")
