import pandas as pd


def clean_data(data):
    """Clean the entered data.
    
    Parameter
    ---------
    data : DataFrame
        The weather data in DataFrame format.
    
    Return
    ------
    df : DataFrame
        A cleaned up DataFrame to give to the machine learning model.    
    """
    if isinstance(data, pd.DataFrame):
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
            'N'	    : 360,

            'Yes'   : 1,
            'No'    : 0
        }

        try:
            data = data.drop(["Evaporation", "Sunshine", "Cloud9am", "Cloud3pm"], axis=1)
        except: 
            pass
        data = data.replace(dict_val)

        new_df = pd.DataFrame()
        for location in data.Location.unique():
            df_location = data[data["Location"] == location]
            df_location = df_location.set_index(['Date'])
            df_location.index = pd.DatetimeIndex(df_location.index)
            df_location = df_location.interpolate(method='time').dropna().reset_index()
            df_location['Location'] = location
            new_df = pd.concat([new_df, df_location])
        
        data = new_df.set_index(['Date', 'Location'])
        data['Month'] = data.index.get_level_values(0).month

        return data
