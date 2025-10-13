import logfire
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from configs import get_settings
from models import User
from models.github import AppRecord, InstallationRecord, Repository

settings = get_settings()

if settings.environment == "test":
    db_url = settings.db_url.rsplit("/", 1)[0] + "/daredevil_test"
else:
    db_url = settings.db_url

_engine = create_async_engine(url=db_url, echo=True, future=True)


async def check_and_create_database():
    """Checks if database exists, if false -> creates database"""

    db_name = (
        "daredevil_test" if settings.environment == "test" else settings.db_name
    )

    postgres_url = settings.db_url.rsplit("/", 1)[0] + "/postgres"
    temp_engine = create_async_engine(postgres_url)

    try:
        async with temp_engine.begin() as connection:
            result = await connection.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                {"db_name": db_name},
            )

            if not result.fetchone():
                await connection.execute(text("COMMIT"))
                await connection.execute(text(f"CREATE DATABASE {db_name}"))
                logfire.info(f"Database {db_name} created")
            else:
                logfire.info(f"Database {db_name} already exists")
    finally:
        await temp_engine.dispose()


async def init_db():
    """Initializes database, creates schema if necessary"""
    await check_and_create_database()
    async with _engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_async_session() -> AsyncSession:
    """Creates and returns an asynchronous database session"""
    _async_session_depot = AsyncSession(_engine)
    return _async_session_depot
