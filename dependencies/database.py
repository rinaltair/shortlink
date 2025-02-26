import asyncio

from sqlalchemy.exc import SQLAlchemyError
from asyncio import TimeoutError
from fastapi import Request
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from configs.settings import settings

engine = create_async_engine(
    settings.DB_CONFIG,
    echo=True,  # Log SQL queries (optional)
    pool_size=5,  # Connection pool size
    pool_pre_ping=True,
    max_overflow=10  # Max connections allowed beyond pool_size
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False  # Prevent attributes from expiring after commit
)

async def check_database_connection(engine: AsyncEngine) -> None:
    try:
        async with engine.connect():
            # Connection is established
            print("Connected to the database")
    except (Exception, TimeoutError, SQLAlchemyError) as e:
        # Connection failed, log the error
        print("Failed to connect to the database")
        print(f"Database connection error: {e}")
        raise

async def get_db(request: Request):
    async with AsyncSessionLocal() as session:
        request.state.db = session
        try:
            yield session
        finally:
            await session.close()