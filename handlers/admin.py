from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext

from database.commands import button as button_db
from database.commands import setting as setting_db
from database.commands import user as user_db
from filters.admin import AdminFilter
from filters import admin as admin_filters
from filters.images import ImageFilter
from keyboards.inline import admin as kbs
from states import admin as admin_states

router = Router(name="admin")


@router.message(Command("admin"), AdminFilter())
async def start_handler(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    user_full_name = await user_db.get_full_name(message.from_user.id)
    user_link = f"<a href='tg://user?id={message.from_user.id}'>{user_full_name}</a>"

    await message.answer(
        text=f"{user_link}, що бажаєте змінити ?",
        reply_markup=kbs.main_keyboard()
    )


@router.callback_query(F.data == "admin_menu", AdminFilter())
async def start_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    user_full_name = await user_db.get_full_name(call.from_user.id)
    user_link = f"<a href='tg://user?id={call.from_user.id}'>{user_full_name}</a>"

    await call.message.answer(
        text=f"{user_link}, що бажаєте змінити ?",
        reply_markup=kbs.main_keyboard()
    )


@router.callback_query(F.data == "change_start_image", AdminFilter())
async def change_image_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer("Вставте нову картинку:", reply_markup=kbs.to_main_menu_kb())
    await state.set_state(admin_states.ChangeImage.image)


@router.message(StateFilter(admin_states.ChangeImage.image), ImageFilter(), AdminFilter())
async def confirm_image_handler(message: types.Message, state: FSMContext) -> None:
    file_id = message.photo[-1].file_id
    await setting_db.set_value("start_image", file_id)
    await message.reply("Успішно збережено!", reply_markup=kbs.to_main_menu_kb())
    await state.clear()


@router.callback_query(F.data == "change_start_text", AdminFilter())
async def change_text_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer("Введіть нове стартове повідомлення:", reply_markup=kbs.to_main_menu_kb())
    await state.set_state(admin_states.ChangeText.text)


@router.message(StateFilter(admin_states.ChangeText.text), AdminFilter())
async def confirm_text_handler(message: types.Message, state: FSMContext) -> None:
    start_text = message.text
    await setting_db.set_value("start_text", start_text)
    await message.reply("Успішно збережено!", reply_markup=kbs.to_main_menu_kb())
    await state.clear()


@router.callback_query(F.data == "admin_show_buttons", AdminFilter())
async def show_buttons_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.answer(
        text="Яку кнопку бажаєте змінити?",
        reply_markup=await kbs.show_buttons_keyboard(create_button=True)
    )


@router.callback_query(F.data == "create_button", AdminFilter())
async def create_button_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(text="Введіть назву:", reply_markup=kbs.to_main_menu_kb())
    await state.set_state(admin_states.AddButton.text)


@router.message(StateFilter(admin_states.AddButton.text), AdminFilter())
async def create_button_handler(message: types.Message, state: FSMContext) -> None:
    await state.update_data(text=message.text)
    await message.reply("Введіть посилання", reply_markup=kbs.to_main_menu_kb())
    await state.set_state(admin_states.AddButton.url)


@router.message(StateFilter(admin_states.AddButton.url), AdminFilter())
async def confirm_button_handler(message: types.Message, state: FSMContext) -> None:
    current_data = await state.get_data()
    text = current_data.get("text")
    await button_db.add_button({
        "text": text,
        "url": message.text
    })

    await message.reply("Додано!", reply_markup=await kbs.show_buttons_keyboard(True))
    await state.clear()


@router.callback_query(admin_filters.OnButtonFilter(), AdminFilter())
async def on_button_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    button_id = int(call.data.split("_")[-1])
    button = await button_db.get_text(button_id)
    await call.message.answer(text=f"Ви вибрали кнопку <b>{button}</b>", reply_markup=kbs.on_button_keyboard(button_id))
    await state.set_state(admin_states.UpdateButton.on_item)
    await state.update_data(button_id=button_id)


@router.callback_query(admin_filters.OnButtonTextFilter(), AdminFilter())
async def update_button_text_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(text=f"Введіть нову назву:")
    await state.set_state(admin_states.UpdateButton.text)


@router.callback_query(admin_filters.OnButtonUrlFilter(), AdminFilter())
async def update_button_url_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    await call.message.answer(text=f"Введіть нове посилання:")
    await state.set_state(admin_states.UpdateButton.url)


@router.callback_query(admin_filters.OnButtonDeleteFilter(), AdminFilter())
async def delete_button_handler(call: types.CallbackQuery, state: FSMContext) -> None:
    button_id = int(call.data.split("_")[-1])
    is_removed = await button_db.delete_by_id(button_id)
    message_text = "Видалено!" if is_removed else "Кнопку не знайдено!"

    await call.message.answer(message_text, reply_markup=await kbs.show_buttons_keyboard(create_button=True))


@router.message(StateFilter(admin_states.UpdateButton.text), AdminFilter())
async def confirm_button_text_handler(message: types.Message, state: FSMContext) -> None:
    current_data = await state.get_data()
    button_id = current_data.get("button_id")
    await button_db.set_text(button_id, message.text)

    await message.reply("Оновлено!", reply_markup=kbs.on_button_keyboard(button_id))


@router.message(StateFilter(admin_states.UpdateButton.url), AdminFilter())
async def confirm_button_url_handler(message: types.Message, state: FSMContext) -> None:
    current_data = await state.get_data()
    button_id = current_data.get("button_id")
    await button_db.set_link(button_id, message.text)

    await message.reply("Оновлено!", reply_markup=kbs.on_button_keyboard(button_id))
