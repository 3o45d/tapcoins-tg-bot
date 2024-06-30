from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


class EnvBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


class BotSettings:
    BOT_TOKEN: str
    ADMIN_LIST: Union[List[Union[int, str]], str] = ''

    @field_validator("ADMIN_LIST", mode='before')
    def parse_admin_list(cls, v: Any) -> List[Union[int, str]]:
        if isinstance(v, str):
            admins = v.split(',')
            return [int(item) if item.isdigit() else item for item in admins]
        elif isinstance(v, list):
            return v
        else:
            raise ValueError("Invalid format for ADMIN_LIST (Check .env)")


class DBSettings(EnvBaseSettings):
    DB_URL: str | None = "sqlite:///test.db"

    @property
    def database_url(self) -> URL | str:
        return self.DB_URL


class Settings(BotSettings, DBSettings):
    DEBUG: bool = False


settings = Settings()

__all__ = ['settings']
