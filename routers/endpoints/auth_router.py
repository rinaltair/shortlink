from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from dependencies.database import get_db
from schemas.token import Token
from services.auth_srv import AuthService
from utils.jwt import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
        data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: AsyncSession = Depends(get_db)
) -> Token:
    service = AuthService(db)
    user = await service.authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token = await service.access_token(user)
    return Token(access_token=access_token, token_type="bearer")
