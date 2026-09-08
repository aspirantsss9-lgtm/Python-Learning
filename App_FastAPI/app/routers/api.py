from fastapi import APIRouter

from app.routers.books import router as books_router


router = APIRouter(prefix="/api")

router.include_router(books_router)