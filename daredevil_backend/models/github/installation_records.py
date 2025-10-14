"""Github App Installation Typed Record Models"""

from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import ConfigDict, EmailStr
from sqlmodel import Field, SQLModel

from models import IDModel, TSModel


class InstallationRecordBase(SQLModel):
    app_id: Optional[int] = Field(default=None)
    app_slug: Optional[str] = Field(default=None)
    access_tokens_url: Optional[str] = Field(default=None)
    html_url: Optional[str] = Field(default=None)
    repositories_url: Optional[str] = Field(default=None)


class InstallationRecordAccountResponse(SQLModel):
    name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    login: Optional[str] = Field(default=None)
    id: Optional[int] = Field(default=None)


class InstallationRecordResponse(InstallationRecordBase):
    model_config = ConfigDict(extra="ignore")

    id: Optional[int] = Field(default=None)
    account: Optional[InstallationRecordAccountResponse] = Field(default=None)
    events: Optional[list[str]] = Field(default=[])


class InstallationRecord(InstallationRecordBase, IDModel, TSModel, table=True):
    __tablename__ = "github_installation_records"
    installation_id: Optional[int] = Field()
