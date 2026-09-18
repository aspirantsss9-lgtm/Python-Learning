from __future__ import annotations

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import create_note, get_notes
from app.database import engine, get_session
from app.models import Base
from app.schemas import NoteCreate


app = FastAPI(
    title="Container Homework",
)

templates = Jinja2Templates(
    directory="app/templates",
)


@app.on_event("startup")
async def startup() -> None:
    """Create database tables on application startup."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


@app.get(
    "/",
    response_class=HTMLResponse,
)
async def index(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> HTMLResponse:
    """Display all notes."""
    notes = await get_notes(session)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"notes": notes},
    )


@app.post("/notes")
async def add_note(
    title: str = Form(...),
    content: str = Form(...),
    session: AsyncSession = Depends(get_session),
) -> RedirectResponse:
    """Create a new note."""
    note_data = NoteCreate(
        title=title,
        content=content,
    )

    await create_note(session, note_data)

    return RedirectResponse(
        url="/",
        status_code=303,
    )


@app.get("/health")
async def health() -> dict[str, str]:
    """Return application health status."""
    return {"status": "ok"}