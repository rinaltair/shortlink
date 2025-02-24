from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from dependencies.database import check_database_connection, engine
from exceptions import ExceptionMiddleware
from routers import router
from utils.seed import seed_db
from utils.limiter import limiter

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
        await seed_db()

    @app.on_event('shutdown')
    async def shutdown():
        await engine.dispose()

    #initialize rate limiter
    app.state.limiter = limiter

    # Register exception handlers
    app.add_middleware(ExceptionMiddleware)
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Include the routers
    app.include_router(router.api_router)

    return app


app = init_app()
