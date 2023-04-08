from __future__ import annotations

from config.config import Env
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


DATABASE_URL = Env.DB_URL


engine = create_async_engine(
    DATABASE_URL,
    poolclass=NullPool,
)
async_session = async_sessionmaker(
    engine, autocommit=False, autoflush=False, expire_on_commit=False
)


async def session() -> AsyncSession:
    async with async_session() as session:
        yield session
