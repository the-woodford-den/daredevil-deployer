"""Github App Typed Record Models"""

from typing import Optional

from pydantic import AliasGenerator, ConfigDict, EmailStr
from sqlmodel import Field, SQLModel

from models import IDModel, TSModel


def serialize(field_name):
    keys = field_name.split("_")
    new_field_name = keys[0] + "".join(x.title() for x in keys[1:])

    return new_field_name


class GitAppBase(SQLModel):
    slug: str = Field()
    node_id: str = Field()
    client_id: Optional[str] = Field(default=None)
    name: str = Field()
    description: Optional[str] = Field(default=None)
    external_url: str = Field()
    html_url: str = Field()


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
    git_id: int = Field(alias="gitId")
    token: Optional[str] = Field(default=None)
    expires_at: Optional[str] = Field(default=None, alias="expiresAt")


class GitAppTokenResponse(SQLModel):
    token: str = Field()
    expires_at: str = Field(alias="expiresAt")


# class AppPermissionsBase(SQLModel):
#     actions: Optional[str] = Field(default=None)
#     actions_variables: Optional[str] = Field(default=None)
#     administration: Optional[str] = Field(default=None)
#     attestations: Optional[str] = Field(default=None)
#     checks: Optional[str] = Field(default=None)
#     contents: Optional[str] = Field(default=None)
#     dependabot_secrets: Optional[str] = Field(default=None)
#     deployments: Optional[str] = Field(default=None)
#     discussions: Optional[str] = Field(default=None)
#     emails: Optional[str] = Field(default=None)
#     environments: Optional[str] = Field(default=None)
#     followers: Optional[str] = Field(default=None)
#     issues: Optional[str] = Field(default=None)
