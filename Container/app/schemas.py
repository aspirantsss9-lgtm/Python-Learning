from __future__ import annotations

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    """Schema for creating a note."""

    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)