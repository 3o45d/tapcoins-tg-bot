from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from database.commands.user import check_is_admin


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        if not message.from_user:
            return False

        user_id = message.from_user.id

        return await check_is_admin(user_id=user_id)


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
