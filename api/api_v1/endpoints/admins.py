"""The admin endpoints."""

from fastapi import APIRouter
from fastapi.params import Depends

from api import deps
from schemas import user_schema


router = APIRouter()

@router.post("/", name="Add a new model",)
async def add_model(current_user: user_schema.User = Depends(deps.get_current_admin_user)):
    """Add a new model.
    """
    return 201
