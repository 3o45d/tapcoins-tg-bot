from aiogram.fsm.state import StatesGroup, State


class ChangeImage(StatesGroup):
    image = State()


class ChangeText(StatesGroup):
    text = State()


class AddButton(StatesGroup):
    text = State()
    url = State()


class UpdateButton(StatesGroup):
    on_item = State()
    text = State()
    url = State()
    confirm = State()
