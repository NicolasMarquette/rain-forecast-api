"""Schemas for the users."""

from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    """Base model for the users."""
    username: Optional[str] = None
    admin: Optional[bool] = None


class UserInDB(User):
    """Model for the hashed_password in the users database."""
    hashed_password: str


