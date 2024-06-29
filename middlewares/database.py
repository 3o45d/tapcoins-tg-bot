from typing import TYPE_CHECKING, Any

from aiogram import BaseMiddleware

from database.database import sessionmaker

from aiogram.types import Update


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Update, data: dict[str, Any]) -> Any:
        async with sessionmaker() as session:
            data["session"] = session
            return await handler(event, data)
