from __future__ import annotations
from typing import TYPE_CHECKING

from pydantic_settings import BaseSettings, SettingsConfigDict

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class BotSettings:
    BOT_TOKEN: str


class DBSettings(EnvBaseSettings):
    DB_URL: str | None = "sqlite:///test.db"

    @property
    def database_url(self) -> URL | str:
        return self.DB_URL


class Settings(BotSettings, DBSettings):
    DEBUG: bool = False


settings = Settings()

__all__ = ['settings']
