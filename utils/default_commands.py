from aiogram.types import BotCommand, BotCommandScopeDefault

bot_commands: dict[str, str] = {
    "start": "Головне меню",
}


async def set_default_commands(bot) -> None:
    await remove_default_commands(bot)

    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in bot_commands.items()
        ],
        scope=BotCommandScopeDefault(),
    )


async def remove_default_commands(bot) -> None:
    await bot.delete_my_commands(scope=BotCommandScopeDefault())
