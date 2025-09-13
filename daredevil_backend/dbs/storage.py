import logfire
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from ..main import get_settings
from ..models import github, user

settings = get_settings.cache_info

_engine = create_async_engine(settings.DB_URL, echo=True, future=True)  # ignore
_async_session_depot = sessionmaker(_engine, class_=AsyncSession)  # ignore


async def init_db():
    async with _engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
