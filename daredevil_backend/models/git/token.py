from typing import Optional

from sqlmodel import Field, SQLModel

from .repositories import RepositoryResponse


class CreateGitAppToken(SQLModel):
    git_id: int = Field()


class GitAppToken(SQLModel):
    token: str = Field()
    expires_at: str = Field(alias="expiresAt")
    permissions: dict[str, str] = Field(default=dict[:])
    repositories: Optional[Optional[RepositoryResponse]] = Field(default=[])
