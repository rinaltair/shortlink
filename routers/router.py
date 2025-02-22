from fastapi import APIRouter
from fastapi.params import Depends

from .endpoints import url, redirect, user, auth
from dependencies.auth import auth_user, auth_active
api_router = APIRouter()  # dependencies=[Depends(Permission().is_allowed_user)])

api_router.include_router(redirect, prefix='', tags=['redirect'])
api_router.include_router(auth, prefix='/api/auth', tags=['auth'])
api_router.include_router(user, prefix='/api/user', tags=['user'], dependencies=[Depends(auth_active)])
api_router.include_router(url, prefix='/api/shortlink', tags=['shortlink'], dependencies=[Depends(auth_user)])
