from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from models import IDModel, TSModel
from utility import serializer


class UserCreate(SQLModel):
    email: EmailStr = Field(default=...)
    username: str = Field(default=...)
    password: str = Field(default=...)


class UserLogin(SQLModel):
    access_token: str = Field(default=...)
    type: str = Field(default=...)


class UserBase(SQLModel):
    access_token: Optional[str] = Field(default=None)
    avatar_url: Optional[str] = Field(default=None)
    client_id: Optional[str] = Field(default=None)
    device_code: Optional[str] = Field(default=None)
    events_url: Optional[str] = Field(default=None)
    expires_in: Optional[str] = Field(default=None)
    followers_url: Optional[str] = Field(default=None)
    following_url: Optional[str] = Field(default=None)
    gists_url: Optional[str] = Field(default=None)
    gravatar_id: Optional[str] = Field(default=None)
    html_url: Optional[str] = Field(default=None)
    interval: Optional[int] = Field(default=None)
    login: Optional[str] = Field(default=None)
    node_id: Optional[str] = Field(default=None)
    organizations_url: Optional[str] = Field(default=None)
    received_events_url: Optional[str] = Field(default=None)
    repos_url: Optional[str] = Field(default=None)
    site_admin: Optional[bool] = Field(default=False)
    starred_url: Optional[str] = Field(default=None)
    subscriptions_url: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    url: Optional[str] = Field(default=None)
    user_code: Optional[str] = Field(default=None)
    user_view_type: Optional[str] = Field(default=None)
    verification_uri: Optional[str] = Field(default=None)


class UserUpdate(UserBase):
    email: Optional[EmailStr] = Field(default=None)
    username: Optional[str] = Field(default=None)
    git_id: Optional[int] = Field(default=None)


class User(UserBase, IDModel, TSModel, table=True):
    model_config = serializer
    __tablename__ = "users"  # type: ignore[reportAssignmentType]
    git_id: int = Field(default=...)
    email: EmailStr = Field(default=...)
    password_hash: str = Field(default=...)
    username: str = Field(default=..., index=True)
