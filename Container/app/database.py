from __future__ import annotations

import os

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@db:5432/container_db",
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():
    """Provide an asynchronous database session."""
    async with SessionLocal() as session:
        yield session