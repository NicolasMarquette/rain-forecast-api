"""Run the API"""

from fastapi import FastAPI

from api.api_v1.api import api_router
from core.config import settings


description = """
## API to get the performance of the machine learning model.

Select the machine learning model for your weather data :  
 
- Gradient Boosting Classifier (`gbc`)  
- K-Nearest Neighbors (`knn`)  
- Decision Tree Classifier (`dtc`)  
- Logistic Regression (`lr`)  
- Gaussian Naive Bayes (`gnb`)

### Made by
* Nicolas Marquette & Marcello Caciolo
* 2021
"""

app = FastAPI(
    title="RAIN FORECAST API",
    description=description,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=[
        {
            "name": "status",
            "description": "check if the API works."
        },
        {
            "name" : "predict",
            "description": "functions to predict from a model of machine learning"
        },
        # To be developped...
        # {
        #     "name": "admins",
        #     "description": "functions for the admins"
        # },
        {
            "name": "login",
            "description": "function to login"
        }
    ]
)


# Call the routers
app.include_router(api_router, prefix=settings.API_V1_STR)
