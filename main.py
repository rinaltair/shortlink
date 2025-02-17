from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer
from starlette.authentication import AuthenticationError

from dependencies.database import check_database_connection, engine
from exceptions import (http, lookup, value, generic, request, auth)
from routers import router


def init_app():
    """
        This is a Skeleton for backend with FastAPI.
    """
    app = FastAPI(
        title="Shortlink API",
        description="API for creating and managing shortlinks.",
        version="1.0.0",
        openapi_url="/api/openapi.json",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
    )

    @app.on_event('startup')
    async def startup():
        await check_database_connection(engine)

    @app.on_event('shutdown')
    async def shutdown():
        await engine.dispose()

    # Register exception handlers
    app.add_exception_handler(HTTPException, http)
    app.add_exception_handler(RequestValidationError, request)
    app.add_exception_handler(ValueError, value)
    app.add_exception_handler(LookupError, lookup)
    app.add_exception_handler(Exception, generic)
    app.add_exception_handler(AuthenticationError, auth)
    app.include_router(router.api_router)

    return app


app = init_app()
