"""The model's prediction route."""

import pandas as pd
from fastapi import APIRouter, File
from fastapi.datastructures import UploadFile
from fastapi.params import Depends
from joblib import load
from sklearn.metrics import balanced_accuracy_score, accuracy_score

from api import deps
from schemas import user_schema, predict_schema, ml_schema


router = APIRouter()


@router.post("/<models>/<target>",
        name="Return the performance of the specified machine learning model",
        response_model=predict_schema.Prediction,
)
async def get_ml_performance(
        models: ml_schema.MlModels,
        target: str,
        file: UploadFile = File(..., description="csv file"),
        current_user: user_schema.User = Depends(deps.get_current_user)
):
    """Get the performance of the specified machine learning model."""
    data = pd.read_csv(file.file)
    X = data.drop(columns=f"{target}")
    y = data[f"{target}"]
    model = load(f"rain-forecast-api/ml-models/{models}.pickle") # a tester
    predict = model.predict(X)
    accuracy = accuracy_score(y, predict)
    balanced_accuracy = balanced_accuracy_score(y, predict)

    result = {
            "model": models,
            "accuracy": accuracy, 
            "balanced_accuracy": balanced_accuracy,
    }

    return result


@router.post("/")
async def get_ml_performance(
        file: UploadFile=File(..., description="csv file"),
        current_user: user_schema.User = Depends(deps.get_current_user)
):
    """Get the performance of the specified machine learning model."""
    data = pd.read_csv(file.file).to_json(orient="records")
    return data
