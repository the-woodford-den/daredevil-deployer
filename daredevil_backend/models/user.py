from typing import Optional

from sqlmodel import Field

from .base import IDModel, TSModel


class User(IDModel, TSModel, table=True):
    __tablename__ = "users"
    access_token: Optional[str] = Field(default=None)
    avatar_url: str = Field()
    client_id: Optional[str] = Field(default=None)
    device_code: Optional[str] = Field(default=None)
    events_url: str = Field()
    expires_in: Optional[str] = Field(default=None)
    followers_url: str = Field()
    following_url: str = Field()
    gists_url: str = Field()
    github_id: int = Field()
    gravatar_id: Optional[str] = Field(default=None)
    html_url: str = Field()
    interval: Optional[int] = Field(default=None)
    login: str = Field()
    node_id: str = Field()
    organizations_url: str = Field()
    received_events_url: str = Field()
    repos_url: str = Field()
    site_admin: bool = Field(default=False)
    starred_url: str = Field()
    subscriptions_url: str = Field()
    type: str = Field()
    url: str = Field()
    user_code: Optional[str] = Field(default=None)
    user_view_type: str = Field()
    verification_uri: Optional[str] = Field(default=None)
