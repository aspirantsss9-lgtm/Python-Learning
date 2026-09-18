from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Note
from app.schemas import NoteCreate


async def get_notes(session: AsyncSession) -> list[Note]:
    """Return all notes ordered by creation time."""
    result = await session.execute(
        select(Note).order_by(Note.id.desc())
    )
    return list(result.scalars().all())


async def create_note(
    session: AsyncSession,
    note_data: NoteCreate,
) -> Note:
    """Create and save a new note."""
    note = Note(
        title=note_data.title,
        content=note_data.content,
    )

    session.add(note)
    await session.commit()
    await session.refresh(note)

    return note