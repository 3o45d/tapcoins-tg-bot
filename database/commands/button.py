from typing import Optional

from sqlalchemy import func, select, update

from database.database import get_session
from database.models import ButtonModel


async def add_button(button: dict) -> None:
    # TODO: button -> typed dict
    async with get_session() as session:
        text: Optional[str] = button.get("text", None)
        link: Optional[str] = button.get("url", None)

        new_button = ButtonModel(
            text=text,
            link=link
        )

        session.add(new_button)
        await session.commit()


async def get_all_buttons() -> list[ButtonModel]:
    async with get_session() as session:
        query = select(ButtonModel)

        result = await session.execute(query)

        buttons = result.scalars()
        return list(buttons)


async def get_by_id(button_id: int) -> ButtonModel:
    async with get_session() as session:
        query = select(ButtonModel).filter_by(id=button_id).limit(1)

        result = await session.execute(query)

        button = result.scalar_one_or_none()
        return button


async def delete_by_id(button_id: int) -> bool:
    async with get_session() as session:
        query = select(ButtonModel).filter_by(id=button_id).limit(1)
        result = await session.execute(query)
        button = result.scalar_one_or_none()

        if button:
            await session.delete(button)
            await session.commit()
            return True
        return False


async def get_text(button_id: int) -> str:
    async with get_session() as session:
        query = select(ButtonModel.text).filter_by(id=button_id)

        result = await session.execute(query)

        text = result.scalar_one_or_none()
        return text or ""


async def get_link(button_id: int) -> str:
    async with get_session() as session:
        query = select(ButtonModel.link).filter_by(id=button_id)

        result = await session.execute(query)

        link = result.scalar_one_or_none()
        return link or ""


async def set_text(button_id: int, text: str) -> None:
    async with get_session() as session:
        stmt = update(ButtonModel).filter_by(id=button_id).values(text=text)

        await session.execute(stmt)
        await session.commit()


async def set_link(button_id: int, link: str) -> None:
    async with get_session() as session:
        stmt = update(ButtonModel).filter_by(id=button_id).values(link=link)

        await session.execute(stmt)
        await session.commit()


async def get_button_count() -> int:
    async with get_session() as session:
        query = select(func.count()).select_from(ButtonModel)

        result = await session.execute(query)

        count = result.scalar_one_or_none() or 0
        return int(count)
