import contextlib
from typing import AsyncIterator, Optional, Type

from pydantic import ConfigDict
from sqlalchemy.ext.asyncio import (AsyncConnection, AsyncEngine,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlmodel import Field, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from configs import get_settings


class DataStoreProps(SQLModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    echo: Optional[bool] = Field(default=True)
    future: Optional[bool] = Field(default=True)
    poolclass: Optional[Type[AsyncAdaptedQueuePool]] = Field(default=None)
    pool_size: Optional[int] = Field(default=10)
    max_overflow: Optional[int] = Field(default=5)
    pool_recycle: Optional[int] = Field(default=3600)


class DataStore:
    def __init__(self, host: str, engine_kwargs: DataStoreProps):
        self._engine: Optional[AsyncEngine] = None
        self._async_sessionmaker: Optional[async_sessionmaker] = None
        self._engine_kwargs: DataStoreProps = engine_kwargs
        self._host: str = host

    def init(self, host: str):
        props = DataStoreProps.model_dump(self._engine_kwargs)
        self._engine = create_async_engine(host, **props)
        self._async_sessionmaker = async_sessionmaker(
            autocommit=False, bind=self._engine
        )

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
data_store_props = DataStoreProps(
    echo=True,
    future=True,
    poolclass=AsyncAdaptedQueuePool,
    pool_size=10,
    max_overflow=5,
    pool_recycle=3600,
)
data_store = DataStore(settings.db_url, data_store_props)


async def get_async_session() -> AsyncIterator[AsyncSession]:
    """Creates and yields an asynchronous database session"""
    async with data_store.session() as session:
        yield session
