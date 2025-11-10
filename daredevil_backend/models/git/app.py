"""Github App Typed Record Models"""

from typing import Optional

from pydantic import AliasGenerator, ConfigDict, EmailStr
from sqlmodel import Field, SQLModel

from models import IDModel, TSModel
from utility import serialize


class GitAppBase(SQLModel):
    description: Optional[str] = Field(default=None)
    external_url: str = Field()
    html_url: str = Field()
    name: str = Field()
    node_id: str = Field()
    slug: str = Field()


class GitAppOwnerResponse(SQLModel):
    id: int
    name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    login: str
    node_id: str = Field()
    avatar_url: str = Field()
    gravatar_id: Optional[str] = Field(default=None)
    html_url: str = Field()
    followers_url: str = Field()
    following_url: str = Field()
    gists_url: str = Field()
    starred_url: str = Field()
    subscriptions_url: str = Field()
    organizations_url: str = Field()
    repos_url: str = Field()
    events_url: str = Field()
    received_events_url: str = Field()
    user_view_type: str = Field()
    site_admin: bool = Field(default=False)
    url: str = Field()
    type: str = Field()


class GitAppPermissionsResponse(SQLModel):
    issues: Optional[str] = Field(default=None)
    checks: Optional[str] = Field(default=None)
    contents: Optional[str] = Field(default=None)
    deployments: Optional[str] = Field(default=None)
    additionalProperties: Optional[str] = Field(default=None)


class GitAppResponse(GitAppBase):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=lambda field_name: (serialize(field_name))
        )
    )

    id: int = Field()
    owner: Optional[GitAppOwnerResponse] = Field(default=None)
    events: list[Optional[str]] = Field(default_factory=list)
    permissions: Optional[GitAppPermissionsResponse] = Field(default=None)


class GitApp(GitAppBase, IDModel, TSModel, table=True):
    __tablename__ = "git_apps"
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=lambda field_name: (serialize(field_name))
        )
    )
    git_id: int = Field(alias="gitId", index=True)


#
