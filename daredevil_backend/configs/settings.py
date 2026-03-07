import os
from typing import Optional, Sequence

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
    allowed_origins: str = Field(default="*")
    app_secret: str = Field(default="secret")
    app_title: str = Field(default="daredevil")
    cc_alg: str = Field(default="cc_alg")
    db_host: str = Field(default="127.0.0.1")
    db_name: str = Field(default="postgres")
    db_port: str = Field(default="5432")
    db_url: str = Field(default="db_url")
    db_user: str = Field(default="postgres")
    domain: str = Field(default="127.0.0.1")
    env: str = Field(default="test")
    gha_secret: str = Field(default="github")
    gha_private_key: Optional[str] = Field(default=None)
    jwt_alg: str = Field(default="hash")
    logfire_token: Optional[str] = Field(default=None)
    redis_port: int = Field(default=6379)
    redis_host: str = Field(default="127.0.0.1")

    @computed_field
    @property
    def allowed_origins_list(self) -> Sequence[str]:
        return tuple(self.allowed_origins.split(","))

    def __getattr__(self, name: str):
        return None


def get_settings() -> Settings:
    return Settings()
