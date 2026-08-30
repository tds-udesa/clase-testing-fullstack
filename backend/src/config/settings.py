from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str
    cors_origins: list[str] = ["*"]


@lru_cache()
def get_settings(env: str | None = None) -> Settings:
    return Settings(_env_file=f".env{f'.{env}' if env else ''}")
