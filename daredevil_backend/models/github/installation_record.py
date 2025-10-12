"""Github App Installation Typed Record Models"""

from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from models import IDModel, TSModel


class InstallationRecordBase(SQLModel):
    events: list[str] = Field()
    app_id: int = Field()
    app_slug: str = Field()
    access_tokens_url: str = Field()
    html_url: str = Field()
    repositories_url: str = Field()


class InstallationRecordAccountResponse(SQLModel):
    name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    login: str
    id: int


class InstallationRecordResponse(InstallationRecordBase):
    id: int = Field()
    account: InstallationRecordAccountResponse = Field()


class InstallationRecord(InstallationRecordBase, IDModel, TSModel, table=True):
    __tablename__ = "github_installation_records"
    installation_id: int = Field()
