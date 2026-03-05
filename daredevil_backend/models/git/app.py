"""Git App Typed Record Models"""

from typing import Optional
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Field, SQLModel
from models import IDModel, TSModel
from utility import serializer


class GitAppBase(SQLModel):
    description: Optional[str] = Field(default=None)
    external_url: str = Field(default=...)
    html_url: str = Field(default=...)
    name: str = Field(default=...)
    node_id: str = Field(default=...)
    slug: str = Field(default=...)


class GitAppOwnerResponse(SQLModel):
    id: int
    name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    login: str
    node_id: str = Field(default=...)
    avatar_url: str = Field(default=...)
    gravatar_id: Optional[str] = Field(default=None)
    html_url: str = Field(default=...)
    followers_url: str = Field(default=...)
    following_url: str = Field(default=...)
    gists_url: str = Field(default=...)
    starred_url: str = Field(default=...)
    subscriptions_url: str = Field(default=...)
    organizations_url: str = Field(default=...)
    repos_url: str = Field(default=...)
    events_url: str = Field(default=...)
    received_events_url: str = Field(default=...)
    user_view_type: str = Field(default=...)
    site_admin: bool = Field(default=False)
    url: str = Field(default=...)
    type: str = Field(default=...)


class GitAppPermissionsResponse(SQLModel):
    issues: Optional[str] = Field(default=None)
    checks: Optional[str] = Field(default=None)
    contents: Optional[str] = Field(default=None)
    deployments: Optional[str] = Field(default=None)
    additionalProperties: Optional[str] = Field(default=None)


class GitAppResponse(GitAppBase):
    model_config = serializer
    id: int = Field(default=...)
    owner: Optional[GitAppOwnerResponse] = Field(default=None)
    events: list[Optional[str]] = Field(default_factory=list)
    permissions: Optional[GitAppPermissionsResponse] = Field(default=None)


class GitApp(GitAppBase, IDModel, TSModel, table=True):
    __tablename__ = "git_apps"  # type: ignore[reportAssignmentType]
    model_config = serializer
    git_id: int = Field(default=..., alias="gitId", index=True)


class GitAppCreate(SQLModel):
    app_slug: str = Field(default=...)
    client_id: str = Field(default=...)


class GitAppRead(SQLModel):
    model_config = serializer
    id: UUID = Field(default=...)
    description: Optional[str] = Field(default=None)
    html_url: str = Field(default=...)
    name: str = Field(default=...)
    slug: str = Field(default=...)
    git_id: int = Field(default=..., alias="gitId", index=True)


#
