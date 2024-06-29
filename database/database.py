from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from core.config import settings

if TYPE_CHECKING:
    from sqlalchemy.engine.url import URL


def get_engine(url: URL | str = "sqlite+aiosqlite:///./test.db") -> AsyncEngine:
    return create_async_engine(
        url=url,
        echo=settings.DEBUG,
        connect_args={
            "check_same_thread": False,
        },
    )


def get_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@asynccontextmanager
async def get_session() -> AsyncSession:
    async with sessionmaker() as session:
        yield session


engine = get_engine(url=f"sqlite+aio{settings.database_url}")
sessionmaker = get_sessionmaker(engine)
