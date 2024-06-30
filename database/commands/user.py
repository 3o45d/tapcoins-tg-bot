from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import func, select, update

from database.database import get_session
from database.models import UserModel

if TYPE_CHECKING:
    from aiogram.types import User


async def add_user(user: User) -> None:
    # TODO: button -> typed dict
    async with get_session() as session:
        user_id: int = user.id
        first_name = user.first_name
        last_name = user.last_name
        username = user.username
        language_code = user.language_code

        new_user = UserModel(
            id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            language_code=language_code,
        )

        session.add(new_user)
        await session.commit()


async def get_all_users() -> list[UserModel]:
    async with get_session() as session:
        query = select(UserModel)

        result = await session.execute(query)

        users = result.scalars()
        return list(users)


async def get_by_id(user_id: int) -> UserModel:
    async with get_session() as session:
        query = select(UserModel).filter_by(id=user_id).limit(1)

        result = await session.execute(query)

        user = result.scalar_one_or_none()
        return user


async def get_by_username(username: str) -> UserModel:
    async with get_session() as session:
        query = select(UserModel).filter_by(username=username).limit(1)

        result = await session.execute(query)

        user = result.scalar_one_or_none()
        return user


async def user_exists(user_id: int) -> bool:
    async with get_session() as session:
        query = select(UserModel.id).filter_by(id=user_id).limit(1)

        result = await session.execute(query)

        user = result.scalar_one_or_none()
        return bool(user)


async def get_full_name(user_id: int) -> str:
    user = await get_by_id(user_id)
    first_name = user.first_name
    last_name = user.last_name

    return f"{first_name} {last_name if last_name else ''}"


async def get_language_code(user_id: int) -> str:
    async with get_session() as session:
        query = select(UserModel.language_code).filter_by(id=user_id)

        result = await session.execute(query)

        language_code = result.scalar_one_or_none()
        return language_code or ""


async def set_language_code(user_id: int, language_code: str) -> None:
    async with get_session() as session:
        stmt = update(UserModel).filter_by(id=user_id).values(language_code=language_code)

        await session.execute(stmt)
        await session.commit()


async def set_first_name(user_id: int, first_name: str) -> None:
    async with get_session() as session:
        stmt = update(UserModel).filter_by(id=user_id).values(first_name=first_name)

        await session.execute(stmt)
        await session.commit()


async def set_last_name(user_id: int, last_name: str) -> None:
    async with get_session() as session:
        stmt = update(UserModel).filter_by(id=user_id).values(last_name=last_name)

        await session.execute(stmt)
        await session.commit()


async def set_username(user_id: int, username: str) -> None:
    async with get_session() as session:
        stmt = update(UserModel).filter_by(id=user_id).values(username=username)

        await session.execute(stmt)
        await session.commit()


async def get_user_count() -> int:
    async with get_session() as session:
        query = select(func.count()).select_from(UserModel)

        result = await session.execute(query)

        count = result.scalar_one_or_none() or 0
        return int(count)
