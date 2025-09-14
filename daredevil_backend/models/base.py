from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, text


class IDModel(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)


class TSModel(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={"server_default": text("current_timestamp(0)")},
    )
    updated_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)"),
            "onupdate": text("current_timestamp(0)"),
        },
    )
