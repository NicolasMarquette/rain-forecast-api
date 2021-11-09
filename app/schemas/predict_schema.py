"""Schema for the prediction."""

import pandas as pd
from pydantic import BaseModel
from typing import List, Any, Dict


# class Prediction(BaseModel):
#     """Base model for the prediction."""
#     model: str
#     accuracy: str
#     balanced_accuracy: str


class Prediction(BaseModel):
    """Base model for the prediction."""
    model: str
    data: List[Dict[str, str]]

# class Config:
#     arbitrary_types_allowed = True
