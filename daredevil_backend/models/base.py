import datetime as dt
from datetime import timezone
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlmodel import Field, SQLModel


class IDModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)


class TSModel(SQLModel):
    created_at: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": func.now()},
    )
    updated_at: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()},
    )
