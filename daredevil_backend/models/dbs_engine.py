from typing import Optional, Type

from pydantic import ConfigDict
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlmodel import Field, SQLModel


class DataStoreProps(SQLModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    echo: Optional[bool] = Field(default=True)
    future: Optional[bool] = Field(default=True)
    poolclass: Optional[Type[AsyncAdaptedQueuePool]] = Field(default=None)
    pool_size: Optional[int] = Field(default=10)
    max_overflow: Optional[int] = Field(default=5)
    pool_recycle: Optional[int] = Field(default=3600)
