from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Provides application settings for each environment"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
        case_sensitive=False,
    )
    # Environment
    environment: str = Field(default="dev")
    # Database
    db_host: str = Field()
    db_name: str = Field()
    db_port: str = Field()
    db_user: str = Field()
    db_url: str = Field()
    # GitHub App
    gha_client_id: Optional[str] = Field(default=None)
    gh_username: Optional[str] = Field(default=None)
    gha_id: Optional[str] = Field(default=None)
    gha_private_key: Optional[str] = Field(default=None)
    # Logfire
    logfire_token: Optional[str] = Field(default=None)

    def __getattr__(self, name: str):
        return None


@lru_cache
def get_settings() -> Settings:
    return Settings()
