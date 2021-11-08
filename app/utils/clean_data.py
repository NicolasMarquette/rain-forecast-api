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

        df = data.drop(["Evaporation", "Sunshine", "Cloud9am", "Cloud3pm"], axis=1)
        df = df.replace(dict_val)

        new_df = pd.DataFrame()
        for location in df.index.get_level_values(0).unique():
            df_location = df.loc[location]
            df_location.index = pd.DatetimeIndex(df_location.index)
            # Drop first line, if first line is a Nan.
            df_location = df_location.interpolate(method='time').dropna().reset_index()
            df_location['Location'] = location
            new_df = pd.concat([new_df, df_location])
        df = new_df.set_index(['Location', 'Date'])

        df['Month'] = df.index.get_level_values(1).month

        return df
