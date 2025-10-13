"""Github App Typed Record Models"""

from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from models import IDModel, TSModel


class AppRecordBase(SQLModel):
    slug: str = Field()
    node_id: str = Field()
    client_id: str = Field()
    name: str = Field()
    description: Optional[str] = Field(default=None)
    external_url: str = Field()
    html_url: str = Field()


class AppRecordOwnerResponse(SQLModel):
    id: int
    name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    login: str
    node_id: str
    avatar_url: str
    gravatar_id: Optional[str] = Field(default=None)
    url: str = Field()
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
    type: str = Field()
    user_view_type: str = Field()
    site_admin: bool = Field(default=False)


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
    github_app_id: int
    token: Optional[str] = Field(default=None)
    expires_at: Optional[str] = Field(default=None)


class AppRecordTokenResponse(SQLModel):
    token: str = Field()
    expires_at: str = Field()


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
