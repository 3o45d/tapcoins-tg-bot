from datetime import datetime

import uvloop
from loguru import logger

from core.loader import bot, dp
from handlers import get_handlers_router
from middlewares import register_middlewares
from utils.default_commands import remove_default_commands, set_default_commands
from utils.default_settings import set_default_settings


async def on_startup() -> None:
    logger.info("Bot starting...")

    register_middlewares(dp)

    dp.include_router(get_handlers_router())

    await set_default_commands(bot)
    await set_default_settings()

    bot_info = await bot.get_me()

    logger.info(f"Name     - {bot_info.full_name}")
    logger.info(f"Username - @{bot_info.username}")
    logger.info(f"ID       - {bot_info.id}")

    logger.info("[ Bot started ]")


async def on_shutdown() -> None:
    logger.info("bot stopping...")

    await remove_default_commands(bot)

    await dp.storage.close()
    await dp.fsm.storage.close()

    await bot.delete_webhook()
    await bot.session.close()

    logger.info("bot stopped")


async def main() -> None:
    logger.add(
        f"logs/{datetime.now().isoformat()}.log",
        level="DEBUG",
        format="{time} | {level} | {module}:{function}:{line} | {message}",
        rotation="100 KB",
        compression="zip",
    )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    uvloop.run(main())
