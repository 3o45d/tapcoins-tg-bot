import re

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from core.config import settings

from sqlalchemy.ext.asyncio import AsyncSession


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


class ChangeTextButtonFilter(BaseFilter):
    async def __call__(self, call: CallbackQuery, session: AsyncSession) -> bool:
        return call.data.startswith('change_text_button_')


class ChangeLinkButtonFilter(BaseFilter):
    async def __call__(self, call: CallbackQuery, session: AsyncSession) -> bool:
        return call.data.startswith('change_link_button_')


class RemoveButtonFilter(BaseFilter):
    async def __call__(self, call: CallbackQuery, session: AsyncSession) -> bool:
        return call.data.startswith('remove_button_')


class UrlFilter(BaseFilter):
    url_pattern = re.compile(
        r'http[s]?://'
        r'(?:(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,})'
    )

    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        is_url = bool(self.url_pattern.search(message.text))
        if not is_url:
            await message.reply("Помилка зчитування посилання!\n\nПаттерн посилання: <b>http[s]://*</b>")
        return is_url
