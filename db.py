from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base for every mapped model. `migrations/env.py` autogenerates against its metadata."""


_engine: AsyncEngine | None = None
_sessionmaker: async_sessionmaker[AsyncSession] | None = None


def init_engine(url: str, echo: bool = False) -> AsyncEngine:
    global _engine, _sessionmaker

    if _engine is not None:
        return _engine

    logger.info("Creating the database engine")
    _engine = create_async_engine(
        url,
        echo=echo,
        pool_pre_ping=True,
        pool_recycle=1800,
        pool_size=5,
        max_overflow=5,
    )
    _sessionmaker = async_sessionmaker(_engine, expire_on_commit=False)

    return _engine


async def dispose_engine() -> None:
    global _engine, _sessionmaker

    if _engine is None:
        return

    logger.info("Disposing of the database engine")
    await _engine.dispose()
    _engine = None
    _sessionmaker = None


@asynccontextmanager
async def session() -> AsyncIterator[AsyncSession]:
    """A transactional session: commits on success, rolls back on any exception."""
    if _sessionmaker is None:
        raise RuntimeError("`init_engine` must be called before opening a session")

    async with _sessionmaker() as s:
        try:
            yield s
            await s.commit()
        except Exception:
            await s.rollback()
            raise
