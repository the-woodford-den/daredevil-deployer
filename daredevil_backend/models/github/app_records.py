"""Github App Typed Record Models"""

from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from models import IDModel, TSModel


class AppRecordBase(SQLModel):
    slug: str = Field()
    node_id: str = Field(alias="nodeId")
    client_id: str = Field(alias="clientId")
    name: str = Field()
    description: Optional[str] = Field(default=None)
    external_url: str = Field(alias="externalUrl")
    html_url: str = Field(alias="htmlUrl")


class AppRecordOwnerResponse(SQLModel):
    id: int
    name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    login: str
    node_id: str = Field(alias="nodeId")
    avatar_url: str = Field(alias="avatarUrl")
    gravatar_id: Optional[str] = Field(default=None, alias="gravatarId")
    html_url: str = Field(alias="htmlUrl")
    followers_url: str = Field(alias="followersUrl")
    following_url: str = Field(alias="followingUrl")
    gists_url: str = Field(alias="gistsUrl")
    starred_url: str = Field(alias="starredUrl")
    subscriptions_url: str = Field(alias="subscriptionsUrl")
    organizations_url: str = Field(alias="organizationsUrl")
    repos_url: str = Field(alias="reposUrl")
    events_url: str = Field(alias="eventsUrl")
    received_events_url: str = Field(alias="receivedEventsUrl")
    user_view_type: str = Field(alias="userViewType")
    site_admin: bool = Field(default=False, alias="siteAdmin")
    url: str = Field()
    type: str = Field()


class AppRecordPermissionsResponse(SQLModel):
    issues: Optional[str] = Field(default=None)
    checks: Optional[str] = Field(default=None)
    contents: Optional[str] = Field(default=None)
    deployments: Optional[str] = Field(default=None)
    additionalProperties: Optional[str] = Field(default=None)


class AppRecordResponse(AppRecordBase):
    id: int = Field()
    owner: Optional[AppRecordOwnerResponse] = Field(default=None)
    events: list[Optional[str]] = Field(default_factory=list)
    permissions: Optional[AppRecordPermissionsResponse] = Field(default=None)


class AppRecord(AppRecordBase, IDModel, TSModel, table=True):
    __tablename__ = "github_app_records"
    github_app_id: int = Field(alias="githubAppId")
    token: Optional[str] = Field(default=None)
    expires_at: Optional[str] = Field(default=None, alias="expiresAt")


class AppRecordTokenResponse(SQLModel):
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
