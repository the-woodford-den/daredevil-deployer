from pydantic import AliasGenerator, ConfigDict
from sqlmodel import Field, SQLModel

from utility import serialize


class CreateGitToken(SQLModel):
    git_id: int = Field()


class GitToken(SQLModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=lambda field_name: (serialize(field_name))
        )
    )
    token: str = Field()
    user_id: str = Field()
