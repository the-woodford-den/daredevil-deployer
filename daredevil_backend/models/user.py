from typing import Optional

from sqlmodel import Field

from .base import IDModel, TSModel


class User(IDModel, TSModel, table=True):
    __tablename__ = "users"
    github_id: Optional[str] = Field(default=None)
    access_token: Optional[str] = Field(default=None)
    client_id: Optional[str] = Field(default=None)
    device_code: Optional[str] = Field(default=None)
    user_code: Optional[str] = Field(default=None)
    verification_uri: Optional[str] = Field(default=None)
    expires_in: Optional[str] = Field(default=None)
    interval: Optional[int] = Field(default=None)
