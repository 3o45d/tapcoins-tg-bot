from typing import Optional, TypedDict

from sqlalchemy import select, update

from database.database import get_session
from database.models import SettingModel


class SettingDict(TypedDict):
    """
    Attributes:
        name (str): The name of the setting.
        value (Optional[str]): The value of the setting, which can be None.
    """
    name: str
    value: Optional[str]


async def add_setting(setting: SettingDict) -> None:
    async with get_session() as session:
        name: str = setting.get("name")
        value: Optional[str] = setting.get("value", None)

        new_setting = SettingModel(
            name=name,
            value=value
        )

        session.add(new_setting)
        await session.commit()


async def get_all_settings() -> list[SettingModel]:
    async with get_session() as session:
        query = select(SettingModel)

        result = await session.execute(query)

        settings = result.scalars()
        return list(settings)


async def get_by_name(name: str) -> SettingModel:
    async with get_session() as session:
        query = select(SettingModel).filter_by(name=name).limit(1)

        result = await session.execute(query)

        setting = result.scalar_one_or_none()
        return setting


async def get_value(name: str) -> str:
    async with get_session() as session:
        query = select(SettingModel.value).filter_by(name=name)

        result = await session.execute(query)

        value = result.scalar_one_or_none()
        return value or ""


async def set_value(name: str, value: str) -> None:
    async with get_session() as session:
        stmt = update(SettingModel).filter_by(name=name).values(value=value)

        await session.execute(stmt)
        await session.commit()
