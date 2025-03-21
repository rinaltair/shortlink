from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from dependencies.database import get_db
from models import User
from schemas.auth_sch import LoginRequest
from schemas.token import Token
from services.auth_srv import AuthService
from utils.limiter import limiter

router = APIRouter()

@router.post("/token")
@limiter.limit("5/minute")
async def login_for_access_token(
        request: Request,
        data : LoginRequest,
        db: AsyncSession = Depends(get_db)
) -> Token:
    service = AuthService(db)
    user = await service.authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token = await service.access_token(user)
    return Token(access_token=access_token, token_type="bearer")