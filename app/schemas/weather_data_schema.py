"""Schema for the weather data"""

from enum import Enum
from typing import List, Any
from pydantic import BaseModel

class WindDirectionEnum(str, Enum):
    N = 'N',
    NNE = 'NNE',
    NE = 'NE',
    ENE = 'ENE',
    E = 'E',
    ESE = 'ESE',
    SE = 'SE',
    SSE = 'SSE',
    S = 'S',
    SSW = 'SSW',
    SW = 'SW',
    WSW = 'WSW',
    W = 'W',
    WNW = 'WNW',
    NW = 'NW',
    NNW = 'NNW'

class WeatherData(BaseModel):
    """
    Base model for the weather observation. \n
    List of tuples of 22 values : \n
    Date,Location,MinTemp,MaxTemp,Rainfall,Evaporation,Sunshine,WindGustDir,WindGustSpeed,WindDir9am,WindDir3pm,WindSpeed9am,WindSpeed3pm,Humidity9am,Humidity3pm,Pressure9am,Pressure3pm,Cloud9am,Cloud3pm,Temp9am,Temp3pm,RainToday 
    """
    data : List[List[Any]]
    