# RAIN FORECAST

### Introduction

An API to know if it will rain tomorrow or not based on different machine learning models.  
The API needs authentication to be used.

the machine learning models avaible are :  
- Gradient Boosting Classifier (`gbc`)  
- K-Nearest Neighbors (`knn`)  
- Decision Tree Classifier (`dtc`)  
- Logistic Regression (`lr`)  
- Gaussian Naive Bayes (`gnb`)


### Structure for the data

The dataset must have the variables below:  
- Date  
- Location  
- MinTemp  
- MaxTemp  
- Rainfall  
- *Evaporation \**  
- *Sunshine \**  
- WindGustDir  
- WindGustSpeed   
- WindDir9am  
- WindDir3pm  
- WindSpeed9am 
- WindSpeed3pm  
- Humidity9am  
- Humidity3pm  
- Pressure9am  
- Pressure3pm  
- *Cloud9am \** 
- *Cloud3pm \**  
- Temp9am  
- Temp3pm  
- RainToday  

\* This variable can be omitted when sending a cleaned csv.


### Folders

**app** : The folder for the API  
**k8s**: The folder to deploy the API on kubernetes   
**test** : The folder for the test of the API  


### Authors

Nicolas MARQUETTE  
Marcello CACIOLO
