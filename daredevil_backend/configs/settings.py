from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Field, SQLModel


class Settings(SQLModel, BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    # GitHub settings
    gha_client_id: Optional[str] = Field(default=None)
    gh_username: Optional[str] = Field(default=None)
    gha_id: Optional[str] = Field(default=None)
    gha_private_key: Optional[str] = Field(default=None)
    logfire_token: Optional[str] = Field(default=None)
    db_host: str = Field()
    db_name: str = Field()
    db_port: str = Field()
    db_user: str = Field()
    db_url: str = Field()

    def __getattr__(self, name: str):
        return None


@lru_cache
def get_settings() -> Settings:
    return Settings()
