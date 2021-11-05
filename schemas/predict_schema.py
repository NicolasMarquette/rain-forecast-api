"""Schema for the prediction."""

from pydantic import BaseModel


class Prediction(BaseModel):
    """Base model for the prediction."""
    model: str
    accuracy: str
    balanced_accuracy: str