from fastapi import FastAPI

from dependencies.database import check_database_connection, engine

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

    return app


app = init_app()