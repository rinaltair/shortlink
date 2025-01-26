from fastapi import FastAPI

from dependencies.database import check_database_connection, engine


# from fastapi.logger import logger as fastapi_logger
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
# from fastapi_pagination import add_pagination
#
# from configs.config import settings
# from routers import api


def init_app():

    description = """
        This is a Skeleton for backend with FastAPI.
    """

    app = FastAPI()

    @app.on_event('startup')
    async def startup():
        is_connected = await check_database_connection(engine)
        if is_connected:
            print("Connected to the database")
        else:
            print("Failed to connect to the database")

    # @app.on_event("startup")
    # async def startup():
    #     pass
    #
    # app.add_middleware(
    #     SQLAlchemyMiddleware,
    #     db_url=settings.DB_CONFIG,
    #     engine_args={
    #         "echo": False,
    #         "pool_pre_ping": True,
    #         "pool_recycle": 1800
    #     },
    # )
    # app.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=["*"],
    #     allow_credentials=False,
    #     allow_methods=["*"],
    #     allow_headers=["*"],
    # )
    #
    # app.include_router(api.api_router, prefix="/skeleton",)
    # add_pagination(app)
    #
    # gunicorn_error_logger = logging.getLogger("gunicorn.error")
    # gunicorn_logger = logging.getLogger("gunicorn")
    # uvicorn_access_logger = logging.getLogger("uvicorn.access")
    # uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
    #
    # fastapi_logger.handlers = gunicorn_error_logger.handlers
    #
    # if __name__ != "__main__":
    #     fastapi_logger.setLevel(gunicorn_logger.level)
    # else:
    #     fastapi_logger.setLevel(logging.DEBUG)

    return app


app = init_app()