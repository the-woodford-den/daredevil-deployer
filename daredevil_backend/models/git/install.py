"""Github App Installation Typed Record Models"""

from typing import Optional

from pydantic import ConfigDict, EmailStr
from sqlmodel import Field, SQLModel

from models import IDModel, TSModel

from .repositories import RepositoryResponse


class GitInstallTokenResponse(SQLModel):
    token: str = Field()
    expires_at: str = Field()
    permissions: dict[str, str] = Field(default=dict[:])
    repositories: Optional[Optional[RepositoryResponse]] = Field(default=[])


class GitInstallBase(SQLModel):
    app_id: Optional[int] = Field(default=None)
    app_slug: Optional[str] = Field(default=None)
    access_tokens_url: Optional[str] = Field(default=None)
    html_url: Optional[str] = Field(default=None)
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
    events: Optional[list[str]] = Field(default=[])


class GitInstall(GitInstallBase, IDModel, TSModel, table=True):
    __tablename__ = "git_installs"
    git_id: Optional[int] = Field()
