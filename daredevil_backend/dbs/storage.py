import logfire
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from ..main import get_settings
from ..models import github, user

settings = get_settings.cache_info
logfire.configure(service_name="database")

# _engine = create_async_engine(settings.DB_URL, echo=True, future=True)
# _async_session_garage = sessionmaker(_engine, class_=AsyncSession)
#
# async with _engine.begin() as connection:
#     await connection.run_sync(SQLModel.metadata.create_all)
