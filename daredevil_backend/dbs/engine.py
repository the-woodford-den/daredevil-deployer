import contextlib
from typing import Any, AsyncIterator
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    async_sessionmaker,
    create_async_engine
)
from sqlmodel.ext.asyncio.session import AsyncSession

# from sqlmodel import SQLModel
from configs import get_settings
# from models import User
# from models.github import AppRecord, InstallationRecord, Repository


class DataStore:
    
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._async_sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DataStore is down")
        await self._engine.dispose()
        self._engine = None
        self._async_sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DataStore is down")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._async_sessionmaker is None:
            raise Exception("DataStore is down")

        session = self._async_sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()




settings = get_settings()
data_store = DataStore(
    settings.db_url, {
    "echo": True,
    "future": True,
    "poolclass": AsyncAdaptedQueuePool,
    "pool_size": 10,
    "max_overflow": 5,
    "pool_recycle": 3600
})

async def get_async_session() -> AsyncSession:
    """Creates and returns an asynchronous database session"""
    async with data_store.session() as session:
        return session

