from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        if not message.from_user:
            return False

        username = message.from_user.username
        user_id = message.from_user.id

        return username in settings.ADMIN_LIST or user_id in settings.ADMIN_LIST


class OnButtonFilter(BaseFilter):
    async def __call__(self, call: CallbackQuery, session: AsyncSession) -> bool:
        return call.data.startswith("select_button_")


class OnButtonTextFilter(BaseFilter):
    async def __call__(self, call: CallbackQuery, session: AsyncSession) -> bool:
        return call.data.startswith("change_text_button_")


class OnButtonUrlFilter(BaseFilter):
    async def __call__(self, call: CallbackQuery, session: AsyncSession) -> bool:
        return call.data.startswith("change_link_button_")


class OnButtonDeleteFilter(BaseFilter):
    async def __call__(self, call: CallbackQuery, session: AsyncSession) -> bool:
        return call.data.startswith("remove_button_")
