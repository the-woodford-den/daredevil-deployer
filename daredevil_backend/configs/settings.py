import os
from typing import Optional

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file=os.getenv("ENVFILE", ".env.dev"),
    env_file_encoding="utf-8",
    extra="ignore",
    case_sensitive=False,
)


class Settings(BaseSettings):
    """Provides application settings for each environment"""

    model_config = _base_config
    allowed_origins: str = Field()
    app_secret: str = Field()
    app_title: str = Field(default=None)
    cc_alg: str = Field()
    client_id: str = Field()
    db_host: str = Field()
    db_name: str = Field()
    db_port: str = Field()
    db_url: str = Field()
    db_user: str = Field()
    domain: str = Field()
    env: str = Field(default="test")
    gha_secret: str = Field()
    gha_private_key: Optional[str] = Field(default=None)
    jwt_alg: str = Field()
    logfire_token: Optional[str] = Field(default=None)
    redis_port: int = Field()
    redis_host: str = Field()

    @computed_field
    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    def __getattr__(self, name: str):
        return None


def get_settings() -> Settings:
    return Settings()
