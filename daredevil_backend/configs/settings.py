from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="allow"
    )

    # GitHub settings
    gh_username: str | None = None
    gha_id: str | None = None
    gha_private_key: str | None = None
    logfire_token: str | None = None
    db_host: str
    db_name: str
    db_port: str
    db_user: str
    db_url: str
    gha_client_id: str

    def __getattr__(self, name: str):
        return None


@lru_cache
def get_settings() -> Settings:
    return Settings()
