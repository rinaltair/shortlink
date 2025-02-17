from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from configs.settings import settings
from dependencies.database import get_db
from models import User
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

        user_reps = UserRepositories(db)
        user = await user_reps.get_by_username(username=token_data.username)
        if user is None:
            raise credentials_exception
        return user
    except Exception:
        raise
        # logger.error("Failed to get the current user")
        # raise credentials_exception

async def get_current_active_user(
        current_user: User =  Depends(get_current_user)
) -> UserResponse:
    """Check if the current user is active"""
    if current_user.is_active is False:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user       

# TO DO: Add the role check

# async def get_current_active_admin(        
#         current_user: User =  Depends(get_current_active)
# ) -> UserResponse:
#     """Check if the current user is active"""
#     if current_user.rule is not 'admin':
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user  

# async def get_current_active_user(
#         current_user: User =  Depends(get_current_active)
# ) -> UserResponse:
#     """Check if the current user is active"""
#     if current_user.is_active is False:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user   