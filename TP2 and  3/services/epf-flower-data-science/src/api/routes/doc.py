from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from src.schemas.message import MessageResponse
import pandas as pd

router = APIRouter()


@router.get("/", include_in_schema=False)
async def redirect_to_documentation():
    return RedirectResponse(url="/docs")
