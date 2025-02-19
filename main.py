from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.authentication import AuthenticationError

from dependencies.database import check_database_connection, engine
from exceptions import ExceptionMiddleware
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
    app.add_middleware(ExceptionMiddleware)

    # Include the routers
    app.include_router(router.api_router)

    return app


app = init_app()
