from __future__ import annotations

import os

from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import sessionmaker


PG_CONN_URI = os.environ.get("SQLALCHEMY_PG_CONN_URI") or (
    "postgresql+asyncpg://postgres:password@localhost/postgres"
)


engine = create_async_engine(
    PG_CONN_URI,
    echo=False,
)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


Session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class User(Base):
    """User model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Post(Base):
    """Post model."""

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    body: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped[User] = relationship(
        back_populates="posts",
    )

