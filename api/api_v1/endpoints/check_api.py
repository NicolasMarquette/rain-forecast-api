"""The API status endpoint."""

from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def get_api_status():
    """Return a message if the API is working."""
    return {"status": "the API works"}