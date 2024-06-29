from collections.abc import Awaitable, Callable
from typing import Any, TYPE_CHECKING

from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger

from database.commands.user import add_user, user_exists


class AuthMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        message: Message = event
        user = message.from_user

        if not user:
            return await handler(event, data)

        if await user_exists(user.id):
            return await handler(event, data)

        logger.info(f"New user registration | user_id: {user.id} | message: {message.text}")

        await add_user(user=user)

        return await handler(event, data)
