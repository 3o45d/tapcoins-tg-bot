from aiogram import Dispatcher
from aiogram.utils.callback_answer import CallbackAnswerMiddleware


def register_middlewares(dp: Dispatcher) -> None:
    from .auth import AuthMiddleware
    from .database import DatabaseMiddleware
    from .logging import LoggingMiddleware

    dp.update.outer_middleware(LoggingMiddleware())

    dp.update.outer_middleware(DatabaseMiddleware())

    dp.callback_query.middleware(AuthMiddleware())
    dp.message.middleware(AuthMiddleware())

    dp.callback_query.middleware(CallbackAnswerMiddleware())
