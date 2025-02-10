from fastapi import APIRouter

from .endpoints import url, redirect, user

api_router = APIRouter()  # dependencies=[Depends(Permission().is_allowed_user)])

api_router.include_router(user, prefix='/api/user', tags=['user'])
api_router.include_router(url, prefix='/api/shortlink', tags=['shortlink'])
api_router.include_router(redirect, prefix='', tags=['redirect'])
