from typing import AsyncGenerator

import logfire
from rich import inspect
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from configs import get_settings
from models import App, User

settings = get_settings()
inspect(settings)
_engine = create_async_engine(url=settings.db_url, echo=True, future=True)


async def check_and_create_database():
    """Check if database exists, create if it doesn't"""
    # Create connection to postgres without database
    postgres_url = settings.db_url.rsplit("/", 1)[0] + "/postgres"
    temp_engine = create_async_engine(postgres_url)

    try:
        async with temp_engine.begin() as connection:
            # Check if database exists
            result = await connection.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                {"db_name": settings.db_name},
            )

            if not result.fetchone():
                # Database doesn't exist, create it
                await connection.execute(text("COMMIT"))
                await connection.execute(
                    text(f"CREATE DATABASE {settings.db_name}")
                )
                logfire.info(f"Database {settings.db_name} created")
            else:
                logfire.info(f"Database {settings.db_name} already exists")
    finally:
        await temp_engine.dispose()


async def init_db():
    await check_and_create_database()
    async with _engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncSession:
    _async_session_depot = AsyncSession(_engine)
    return _async_session_depot
