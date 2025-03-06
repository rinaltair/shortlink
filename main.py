from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from dependencies.database import check_database_connection, engine
from exceptions import ExceptionMiddleware
from middlewares.async_cleanup_mid import AsyncCleanupMiddleware
from routers import router
from utils.limiter import limiter
from utils.seed import seed_db

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

    origins = [
        "http://localhost",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    @app.on_event('startup')
    async def startup():
        await check_database_connection(engine)
        await seed_db()

    @app.on_event('shutdown')
    async def shutdown():
        await engine.dispose()

    # Initialize rate limiter
    app.state.limiter = limiter

    # Register exception handlers
    app.add_middleware(AsyncCleanupMiddleware)
    app.add_middleware(ExceptionMiddleware)
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Include the routers
    app.include_router(router.api_router)

    return app


app = init_app()
