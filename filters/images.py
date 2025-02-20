from __future__ import annotations
from aiogram.filters import BaseFilter

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiogram.types import Message
    from sqlalchemy.ext.asyncio import AsyncSession


class ImageFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        if not message.photo:
            await message.answer(f"Помилка считування зображення, спробуйте ще раз!")
            return False

        return True
