"""API Router for Fast API."""
from fastapi import APIRouter
from src.api.routes import hello, doc, data
from fastapi.responses import RedirectResponse

router = APIRouter()


router.include_router(hello.router, tags=["Hello"])
router.include_router(doc.router, tags=["Documentation"])
router.include_router(data.router, tags=["Data"])


@router.get("/")
async def root():
    return RedirectResponse(url="/docs")