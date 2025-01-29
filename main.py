from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from dependencies.database import check_database_connection, engine
from routers import router
from exceptions import (http, lookup,value,generic, request)

def init_app():

    """
        This is a Skeleton for backend with FastAPI.
    """

    app = FastAPI()

    @app.on_event('startup')
    async def startup():
        await check_database_connection(engine)

    @app.on_event('shutdown')
    async def shutdown():
        await engine.dispose()

    # Register exception handlers
    app.add_exception_handler(HTTPException, http)
    app.add_exception_handler(RequestValidationError, request)

    app.include_router(router.api_router)
    return app

app = init_app()