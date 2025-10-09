from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from .base import IDModel, TSModel

if TYPE_CHECKING:
    from .github import App  # AppOwner, Repository


class User(IDModel, TSModel, table=True):
    access_token: Optional[str] | None = Field(default=None)
    client_id: Optional[str] | None = Field(default=None)
    device_code: Optional[str]
    user_code: Optional[str]
    verification_uri: Optional[str]
    expires_in: Optional[int]
    interval: Optional[int]
    # github_owner_id: int
    # repositories: Optional[List["Repository"]] = Relationship(back_populates="user")
    # app_id: UUID | None = Field(default=None, foreign_key="app.id")
    # app: "App" = Relationship(back_populates="user")
    # login: str
    # node_id: str
    # avatar_url: str
    # gravatar_id: str
    # url: str
    # html_url: str
    # followers_url: str
    # following_url: str
    # gists_url: str
    # starred_url: str
    # subscriptions_url: str
    # organizations_url: str
    # repos_url: str
    # events_url: str
    # received_events_url: str
    # type: str
    # user_view_type: str
    # site_admin: bool
