from fastapi import APIRouter, Depends

from .endpoints import url, redirect

api_router = APIRouter()  # dependencies=[Depends(Permission().is_allowed_user)])

api_router.include_router(url, prefix='/api/shortlink', tags=['shortlink'])
api_router.include_router(redirect, prefix='', tags=['redirect'])