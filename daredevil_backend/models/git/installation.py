"""Git Installation Typed Record Models"""

from typing import Optional

from pydantic import ConfigDict, EmailStr
from sqlmodel import Field, SQLModel

from models import IDModel, TSModel
from utility import serializer


class GitInstallationBase(SQLModel):
    app_slug: str = Field(default=None)
    access_tokens_url: Optional[str] = Field(default=None)
    html_url: str = Field(default=None)
    repositories_url: Optional[str] = Field(default=None)


class GitInstallationAccountResponse(SQLModel):
    name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    login: Optional[str] = Field(default=None)
    id: Optional[int] = Field(default=None)


class GitInstallationResponse(GitInstallationBase):
    model_config = ConfigDict(extra="ignore")

    id: Optional[int] = Field(default=None)
    account: Optional[GitInstallationAccountResponse] = Field(default=None)
    app_id: int = Field(default=None)
    events: Optional[list[str]] = Field(default=[])


class GitInstallation(GitInstallationBase, IDModel, TSModel, table=True):
    __tablename__ = "git_installations"
    model_config = serializer
    git_app_id: int = Field()
    git_id: int = Field()
    username: str = Field()


class GitInstallationCreate(SQLModel):
    username: str = Field()


class GitInstallationRead(SQLModel):
    model_config = serializer
    app_slug: str = Field()
    repositories_url: Optional[str] = Field(default=None)
    html_url: str = Field()
    git_id: int = Field(alias="gitId", index=True)
