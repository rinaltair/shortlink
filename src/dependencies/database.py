import asyncio

import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from asyncio import TimeoutError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from src.configs.settings import settings

engine = create_async_engine(
    settings.DB_CONFIG,
    echo=True,  # Log SQL queries (optional)
    pool_size=20,  # Connection pool size
    pool_pre_ping=True,
    max_overflow=50  # Max connections allowed beyond pool_size
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False  # Prevent attributes from expiring after commit
)

async def check_database_connection(engine: AsyncEngine) -> bool:
    try:
        async with engine.connect() as connection:
            # Connection is established, return True
            return True
    except (Exception, TimeoutError, SQLAlchemyError) as e:
        # Connection failed, log the error and return False
        print(f"Database connection error: {e}")
        return False

async def main():
    is_connected = await check_database_connection(engine)
    if is_connected:
        print("Connected to the database")
    else:
        print("Failed to connect to the database")

if __name__ == "__main__":
    asyncio.run(main())