from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from dependencies.database import get_db
from dependencies.auth import auth_user
from models.user_model import User, UserRole
from repositories import UrlRepositories

async def authorize_url(
    id: UUID,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_user)
) -> None:
    url = await UrlRepositories(db).get(id)
    if not url: raise LookupError('Shortlink not found')

    if user.role == UserRole.admin:
        return id
    if user.role == UserRole.user and user.id == url.user_id:
        return id

    raise PermissionError("You are not authorized to perform this action")
