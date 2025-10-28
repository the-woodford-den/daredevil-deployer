from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel


class GitTokenResponse(SQLModel):
    access_token: str = Field()
    token_type: str = Field()
    scope: str = Field()


class GitCreateTokenResponse(SQLModel):
    device_code: str = Field()
    user_code: str = Field()
    verification_uri: str = Field()
    expires_in: int = Field()
    interval: int = Field()
