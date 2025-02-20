from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from configs.settings import settings
from dependencies.database import get_db
from models.user_model import User, UserRole
from repositories import UserRepositories
from utils.jwtmanager import JWTManager
from schemas.user_sch import UserResponse


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Get the current user from the access token"""
    try: 
        token_data = await JWTManager().verify_token(token)

        user = await UserRepositories(db).get_by_username(username=token_data.username)
        if user is None: raise credentials_exception
        return user
    except Exception:
        raise

async def auth_active(
        current_user: User =  Depends(get_current_user)
) -> UserResponse:
    """Check if the current user is active"""
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user       

# TO DO: Add the role check

async def check_role(
    allowed_roles: list[UserRole],
    current_user: User = Depends(auth_active)
) -> UserResponse:
    """Check if the role is allowed"""
    if current_user.role not in allowed_roles:
        raise PermissionError("You are not authorized to perform this action")
    return current_user
    
async def auth_admin(current_user: User =  Depends(auth_active)) -> UserResponse:
    await check_role(allowed_roles=[UserRole.admin], current_user=current_user)

async def auth_user(current_user: User =  Depends(auth_active)) -> UserResponse:
    await check_role(allowed_roles=[UserRole.user], current_user=current_user)
