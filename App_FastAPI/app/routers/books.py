from fastapi import APIRouter, status
from pydantic import BaseModel


router = APIRouter(prefix="/books", tags=["Books"])


class Book(BaseModel):
    title: str
    author: str
    year: int


@router.get("/")
async def get_books():
    return {"message": "List of books"}


@router.get("/{book_id}/")
async def get_book(book_id: int):
    return {"book_id": book_id}


@router.post(
    "/",
    response_model=Book,
    status_code=status.HTTP_201_CREATED,
)
async def create_book(book: Book):
    return book