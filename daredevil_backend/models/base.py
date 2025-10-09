from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlmodel import Column, DateTime, Field, SQLModel


class IDModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)


class TSModel(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    )
