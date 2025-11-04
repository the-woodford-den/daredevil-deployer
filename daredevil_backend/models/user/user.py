from typing import Optional

from sqlmodel import Field, SQLModel

from models import IDModel, TSModel


class UserLogin(SQLModel):
    access_token: str = Field()
    type: str = Field()


class UserBase(SQLModel):
    access_token: Optional[str] = Field(default=None)
    avatar_url: Optional[str] = Field()
    client_id: Optional[str] = Field(default=None)
    device_code: Optional[str] = Field(default=None)
    events_url: Optional[str] = Field()
    expires_in: Optional[str] = Field(default=None)
    followers_url: Optional[str] = Field()
    following_url: Optional[str] = Field()
    gists_url: Optional[str] = Field()
    gravatar_id: Optional[str] = Field(default=None)
    html_url: Optional[str] = Field()
    interval: Optional[int] = Field(default=None)
    login: Optional[str] = Field()
    node_id: Optional[str] = Field()
    organizations_url: Optional[str] = Field()
    received_events_url: Optional[str] = Field()
    repos_url: Optional[str] = Field()
    site_admin: Optional[bool] = Field(default=False)
    starred_url: Optional[str] = Field()
    subscriptions_url: Optional[str] = Field()
    type: Optional[str] = Field()
    url: Optional[str] = Field()
    user_code: Optional[str] = Field(default=None)
    user_view_type: Optional[str] = Field()
    verification_uri: Optional[str] = Field(default=None)


class UserCreate(UserBase):
    username: str = Field()
    password: str = Field()


class UserUpdate(UserBase):
    git_id: int = Field()


class User(UserBase, IDModel, TSModel, table=True):
    __tablename__ = "users"
    username: str = Field()
    password_hash: str = Field()
