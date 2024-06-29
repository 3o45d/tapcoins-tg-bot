from aiogram import Router, types
from aiogram.filters import CommandStart

from database.commands import user as user_db
from database.commands import setting as setting_db
from keyboards.inline.start import main_keyboard

router = Router(name="start")


@router.message(CommandStart())
async def start_handler(message: types.Message) -> None:
    user_full_name = await user_db.get_full_name(message.from_user.id)
    user_link = f"<a href='tg://user?id={message.from_user.id}'>{user_full_name}</a>"
    start_text = await setting_db.get_value('start_text')
    start_message = f"{user_link}, {start_text}"

    image = await setting_db.get_value('start_image')
    if image:
        await message.answer_photo(photo=image, caption=start_message, reply_markup=await main_keyboard())
    else:
        await message.answer(start_message, reply_markup=await main_keyboard())
