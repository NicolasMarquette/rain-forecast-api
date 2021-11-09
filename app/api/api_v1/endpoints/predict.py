"""The model's prediction route."""

import json
from os import stat
import warnings

import joblib
import pandas as pd
from fastapi import APIRouter, File
from fastapi.datastructures import UploadFile
from fastapi.params import Depends
from fastapi import HTTPException, status

from sklearn.metrics import balanced_accuracy_score, accuracy_score
from datetime import timedelta

from api import deps
from schemas import user_schema, predict_schema, ml_schema, weather_data_schema, errors_schema
from utils import clean_data


router = APIRouter()


@router.post("", responses=errors_schema.RESPONSES)
async def predict_rain_tomorrow(
        models : ml_schema.MlModels,
        weather_data : weather_data_schema.WeatherData,
        current_user: user_schema.User = Depends(deps.get_current_user)
):
    """Get the predicted rain for tomorrow basing on weather data observation(s)"""

    #Create a model-like dataframe
    df = pd.DataFrame(weather_data.data, columns = ['Date', 'Location',
                                                    'MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine',
                                                    'WindGustDir', 'WindGustSpeed', 'WindDir9am', 'WindDir3pm',
                                                    'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm',
                                                    'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Temp9am',
                                                    'Temp3pm', 'RainToday'])
    df = df.set_index(['Location', 'Date'])

    try:
            df['Month'] = pd.to_datetime(df.index.get_level_values(1)).month
    except:
            raise HTTPException(status_code=500, detail='Bad data format in one of the Date Field (field 1)')



    #Replace categorical values, drop unused columns and normalize
    dict_val = {
            'N'     : 0,
            'NNE'   : 22.5,
            'NE'    : 45,
            'ENE'   : 67.5,
            'E'     : 90,
            'ESE'   : 112.5,
            'SE'    : 135,
            'SSE'   : 157.5,
            'S'     : 180,
            'SSW'   : 202.5,
            'SW'    : 225,
            'WSW'   : 247.5,
            'W'     : 270,
            'WNW'	: 292.5,
            'NW'	: 315,
            'NNW'	: 337.5,
            'N'	: 360,

            'Yes'   : 1,
            'No'    : 0
    }
    df = df.replace(dict_val)
    df = df.drop(["Evaporation", "Sunshine", "Cloud9am", "Cloud3pm"], axis=1)

    x = df

    with open(f"ml-models/{models}.pickle", "rb") as file:
            model = joblib.load(file)

    #Output dataframe
    df_out = pd.DataFrame()
    df_out['Date'] = (pd.to_datetime(df.index.get_level_values(1)) + timedelta(days=1))
    df_out['Date'] = df_out['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
    df_out['Location'] = df.index.get_level_values(0)
    df_out['RainTomorrow'] = ['Yes' if rt==1 else 'No' for rt in model.predict(x).tolist()]

    return {'RainTomorrow' : df_out.to_dict(orient='split')['data']}


@router.post("/clean",
        name="Return the prediction for a cleaned csv dataset.",
        response_model=predict_schema.Prediction,
        responses=errors_schema.RESPONSES,
)
async def get_ml_performance(
        models: ml_schema.MlModels,
        file: UploadFile = File(..., description="csv file"),
        current_user: user_schema.User = Depends(deps.get_current_user)
):
    """"Get the predicted rain for tomorrow basing on weather data from cleaned csv."""
    data = pd.read_csv(file.file, index_col=[1,0])
    
    with open(f"ml-models/{models}.pickle", "rb") as file:
            model = joblib.load(file)
    
    try:
        warnings.filterwarnings("ignore")
        predict = model.predict(data)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Incorrect data format: the data is not cleaned.",
        )
    
    pred_list = predict.tolist()
    
    list_keys = list(
            (pd.to_datetime(data.index.get_level_values(0)) + timedelta(days=1)).strftime('%Y-%m-%d')
            + '/' + data.index.get_level_values(1)
    )
    
    pred_result = list()
    for keys, pred in zip(list_keys, pred_list):
        pred_result.append({keys: 'Yes' if pred==1 else 'No'})
    result = {
            "model": models,
            "data": pred_result
    }
    return result


@router.post("/raw",
        name="Return the prediction for a raw csv dataset.",
        response_model=predict_schema.Prediction,
        responses=errors_schema.RESPONSES,
)
async def get_ml_performance(
        models: ml_schema.MlModels,
        file: UploadFile = File(..., description="csv file"),
        current_user: user_schema.User = Depends(deps.get_current_user)
):
    """Get the predicted rain for tomorrow basing on weather data from raw csv."""
    df = pd.read_csv(file.file)
    
    data = clean_data.clean_data(df)
    
    with open(f"ml-models/{models}.pickle", "rb") as file:
            model = joblib.load(file)
    
    try:
        warnings.filterwarnings("ignore")
        predict = model.predict(data)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Incorrect data format: the data is not cleaned.",
        )
        
    pred_list = predict.tolist()
    
    list_keys = list(
            (pd.to_datetime(data.index.get_level_values(0)) + timedelta(days=1)).strftime('%Y-%m-%d')
            + '/' + data.index.get_level_values(1)
    )
    
    pred_result = list()
    for keys, pred in zip(list_keys, pred_list):
        pred_result.append({keys: 'Yes' if pred==1 else 'No'})
    result = {
            "model": models,
            "data": pred_result
    }
    return result
