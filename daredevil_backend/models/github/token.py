from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel


class OAuthAccessTokenResponse(SQLModel):
    access_token: str = Field()
    token_type: str = Field()
    scope: str = Field()


class CreateTokenResponse(SQLModel):
    device_code: str = Field()
    user_code: str = Field()
    verification_uri: str = Field()
    expires_in: int = Field()
    interval: int = Field()


class UserResponse(SQLModel):
    id: UUID = Field()
    device_code: str = Field()
    user_code: str = Field()
    verification_uri: str = Field()
    expires_in: int = Field()
    interval: int = Field()
    client_id: Optional[str] = Field(default=None)
    access_token: Optional[str] = Field(default=None)
