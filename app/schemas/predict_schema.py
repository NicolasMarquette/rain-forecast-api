"""Schema for the prediction."""

import pandas as pd
from pydantic import BaseModel


# class Prediction(BaseModel):
#     """Base model for the prediction."""
#     model: str
#     accuracy: str
#     balanced_accuracy: str


class Prediction(BaseModel):
    """Base model for the prediction."""
    model: str
    data: list

# class Config:
#     arbitrary_types_allowed = True
