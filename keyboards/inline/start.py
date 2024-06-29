from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.commands import button as db_button


async def main_keyboard() -> InlineKeyboardMarkup:
    exists_buttons = await db_button.get_all_buttons()
    buttons = [
        [
            InlineKeyboardButton(text=button.text, url=button.link)
        ] for button in exists_buttons
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    keyboard.adjust(2, repeat=True)
    return keyboard.as_markup()
