from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.commands import button as db_button

ADMIN_MENU_BUTTON = [InlineKeyboardButton(text="В головне меню", callback_data="admin_menu")]


def to_main_menu_kb() -> InlineKeyboardMarkup:
    """Use in main menu."""
    buttons = [ADMIN_MENU_BUTTON]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    return keyboard.as_markup()


def main_keyboard() -> InlineKeyboardMarkup:
    """Use in main menu."""
    buttons = [
        [InlineKeyboardButton(text="Картинка повідомлення", callback_data="change_start_image")],
        [InlineKeyboardButton(text="Текст повідомлення", callback_data="change_start_text")],
        [InlineKeyboardButton(text="Кнопки", callback_data="admin_show_buttons")],
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)

    keyboard.adjust(1, 1, 1)

    return keyboard.as_markup()


async def show_buttons_keyboard(create_button: bool = False) -> InlineKeyboardMarkup:
    """Use in main menu."""
    exists_buttons = await db_button.get_all_buttons()
    buttons = [
        [
            InlineKeyboardButton(text=button.text, callback_data=f"select_button_{button.id}")
        ] for button in exists_buttons
    ]

    if create_button:
        buttons.append(
            [InlineKeyboardButton(text="Додати нову кнопку", callback_data="create_button")],
        )

    buttons.append(ADMIN_MENU_BUTTON)

    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()


def on_button_keyboard(button_id: int) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Змінити назву", callback_data=f"change_text_button_{button_id}")],
        [InlineKeyboardButton(text="Змінити посилання", callback_data=f"change_link_button_{button_id}")],
        [InlineKeyboardButton(text="Видалити", callback_data=f"remove_button_{button_id}")],
        [InlineKeyboardButton(text="Назад", callback_data=f"admin_show_buttons")]
    ]

    keyboard = InlineKeyboardBuilder(markup=buttons)
    return keyboard.as_markup()
