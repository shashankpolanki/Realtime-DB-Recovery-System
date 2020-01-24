"""
Algorithm Name: Low-pass filters

Description: Takes a rolling average of a time-series
and removes anamolies based on Z-score
"""

import pandas as pd
import matplotlib.pyplot as plt
import eia

def retrieve_time_series(api, series_ID):
    """
    Return time series dataframe based on API and unique
    Series ID

    Returns: Dataframe
    """
     #Retrieve Data By Series ID
    series_search = api.data_by_series(series=series_ID)
    ##Create a pandas dataframe from the retrieved time series
    df = pd.DataFrame(series_search)
    return df

def scatterplot(x_data, y_data, x_label, y_label, title):
    fig, ax = plt.subplots()
    ax.scatter(x_data, y_data, s = 30, color = '#539caf', alpha = 0.75)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    fig.autofmt_xdate()


if __name__ == "__main__":
    api_key = 'YOUR API KEY HERE'
    api = eia.API(api_key)

    #Pull the oil WTI price data
    series_ID='PET.EER_EPMRU_PF4_RGC_DPG.D'
    gasoline_price_df=retrieve_time_series(api, series_ID)
    gasoline_price_df.reset_index(level=0, inplace=True)
    #Rename the columns for easer analysis
    gasoline_price_df.rename(columns={'index':'Date',
                gasoline_price_df.columns[1]:'Gasoline_Price'},
                inplace=True)

    #Visualize anomalies using matplotlib function
    scatterplot(gasoline_price_df['Date'],
                    gasoline_price_df['Gasoline_Price'],
                    'Date',
                    'Gasoline Price (Dollars Per Gallon)',
                    'US Gulf Coast Gasoline Price Time Series: 2014-Present')
