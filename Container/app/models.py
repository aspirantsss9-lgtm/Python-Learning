from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


class Note(Base):
    """Database model for a note."""

    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )