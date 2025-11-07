from datetime import datetime

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
    client_id: str = Field()
    user_id: str = Field()
    install_id: str = Field()


class DaredevilToken(SQLModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=lambda field_name: (serialize(field_name))
        )
    )
    token: str = Field()
    client_id: str = Field()
    user_id: str = Field()
    expires_at: datetime = Field()
    username: str = Field()


# not being used atm
# class GitTokenResponse(SQLModel):
#     access_token: str = Field()
#     token_type: str = Field()
#     scope: str = Field()
#
#
# class GitCreateTokenResponse(SQLModel):
#     model_config = ConfigDict(
#         alias_generator=AliasGenerator(
#             serialization_alias=lambda field_name: (serialize(field_name))
#         )
#     )
#     device_code: str = Field()
#     user_code: str = Field()
#     verification_uri: str = Field()
#     expires_in: int = Field()
#     interval: int = Field()
