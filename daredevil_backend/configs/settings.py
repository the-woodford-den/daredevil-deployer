from typing import Optional

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Provides application settings for each environment"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
        case_sensitive=False,
    )
    allowed_origins: str

    @computed_field
    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    app_title: str = Field(default=None)
    db_host: str = Field()
    db_name: str = Field()
    db_port: str = Field()
    db_url: str = Field()
    db_user: str = Field()
    environment: str = Field(default="test")
    github_app_secret: str = Field()
    gha_private_key: Optional[str] = Field(default=None)
    logfire_token: Optional[str] = Field(default=None)

    def __getattr__(self, name: str):
        return None


def get_settings() -> Settings:
    return Settings()
