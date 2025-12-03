from sqlmodel import Field, SQLModel

from utility import serializer


class CreateGitToken(SQLModel):
    git_id: int = Field()


class GitToken(SQLModel):
    model_config = serializer
    token: str = Field()
    user_id: str = Field()
