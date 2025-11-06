"""Github App Installation Typed Record Models"""

from typing import Optional

from pydantic import AliasGenerator, ConfigDict, EmailStr
from sqlmodel import Field, SQLModel

from models import IDModel, TSModel
from utility import serialize


class GitInstallBase(SQLModel):
    app_slug: str = Field(default=None)
    access_tokens_url: Optional[str] = Field(default=None)
    html_url: str = Field(default=None)
    repositories_url: Optional[str] = Field(default=None)


class GitInstallAccountResponse(SQLModel):
    name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    login: Optional[str] = Field(default=None)
    id: Optional[int] = Field(default=None)


class GitInstallResponse(GitInstallBase):
    model_config = ConfigDict(extra="ignore")

    id: Optional[int] = Field(default=None)
    account: Optional[GitInstallAccountResponse] = Field(default=None)
    app_id: int = Field(default=None)
    events: Optional[list[str]] = Field(default=[])


class GitInstall(GitInstallBase, IDModel, TSModel, table=True):
    __tablename__ = "git_installs"
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=lambda field_name: (serialize(field_name))
        )
    )
    git_app_id: int = Field()
    git_id: int = Field()
    username: str = Field()
