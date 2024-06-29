from database.commands import setting as db_settings

default_settings: dict[str, str] = {
    "start_text": "Вам надали доступ до ігр, які зможуть насипати:",
    "start_image": None,
}


async def set_default_settings() -> None:
    current_settings = await db_settings.get_all_settings()

    for name, value in default_settings.items():
        if name not in [setting.name for setting in current_settings]:
            await db_settings.add_setting({"name": name, "value": value})
