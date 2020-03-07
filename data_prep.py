import csv
import os
import pandas as pd
import numpy as np
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *


Base = declarative_base()
#engine = create_engine(os.environ['DATABASE_URL_WEATHER']) 
engine = create_engine('postgresql://postgres:Dfcbktr1@localhost:5432/weather')
conn = engine.connect()


def melt_wmo_data(filepath, filename, cols):
    id_vars = ['Country or Territory',
                'Station Name',
                'WMO Station Number',
                'Statistic Description',
                'Unit',
                'dtype']
    df = pd.read_csv(filepath+filename)
    df = df[cols]
    df = pd.melt(df, id_vars=id_vars)
    #df.to_csv(filepath+f'{filename[:-4]}_melted.csv')
    df.to_sql('climate_normals', con=engine)


def pivot_wmo_data(filepath, filename):
    df = pd.read_csv(filepath+filename)
    df['IWMO'] = df['WMO Station Number'] * 10
    df = df.drop(columns=['Statistic Description', 
                            'Unit', 
                            'dtype', 
                            'Country or Territory', 
                            'Station Name', 
                            'WMO Station Number'])
    df['Datatype'] = df['Datatype'].str.replace(' ', '_')

    df['Datatype'] = df['Datatype'].str.lower()
    
    df = df.rename(columns={'IWMO': 'iwmo', 'Month': 'month'})

    df_pivoted = pd.pivot_table(df, index=['iwmo', 'month'], columns=['Datatype'], values='Value', fill_value=-9999.0)
    df_pivoted = df_pivoted.filter(['iwmo', 'month', 'Datatype', 'Value',
                    'mean_temp_mean_value', 
                    'mean_max_temp_mean_value', 
                    'mean_min_temp_mean_value', 
                    'humidity_mean_value', 
                    'precipitation_data_mean_monthly_value', 
                    'sunshine_mean_number_of_hours'])
    df = df.rename(columns={'precipitation_data_mean_monthly_value': 'precipitation_mean_monthly_value'})
    df_pivoted.to_csv('./data/all_data_concat_melted_mod_pivoted.csv')
    #df_pivoted.to_sql('climate_normals', con=engine, if_exists='replace')


# made by https://github.com/anttilipp
def daylength(dayOfYear, lat):
    """Computes the length of the day (the time between sunrise and
    sunset) given the day of the year and latitude of the location.
    Function uses the Brock model for the computations.
    For more information see, for example,
    Forsythe et al., "A model comparison for daylength as a
    function of latitude and day of year", Ecological Modelling,
    1995.
    Parameters
    ----------
    dayOfYear : int
        The day of the year. 1 corresponds to 1st of January
        and 365 to 31st December (on a non-leap year).
    lat : float
        Latitude of the location in degrees. Positive values
        for north and negative for south.
    Returns
    -------
    d : float
        Daylength in hours.
    """
    latInRad = np.deg2rad(lat)
    declinationOfEarth = 23.45*np.sin(np.deg2rad(360.0*(283.0+dayOfYear)/365.0))
    if -np.tan(latInRad) * np.tan(np.deg2rad(declinationOfEarth)) <= -1.0:
        return 24.0
    elif -np.tan(latInRad) * np.tan(np.deg2rad(declinationOfEarth)) >= 1.0:
        return 0.0
    else:
        hourAngle = np.rad2deg(np.arccos(-np.tan(latInRad) * np.tan(np.deg2rad(declinationOfEarth))))
        return 2.0*hourAngle/15.0


#melt_wmo_data('sunshine.csv')

# for filename in os.listdir('./wmo_climate_normals'):
#     df = pd.read_csv('./wmo_climate_normals/'+filename)
#     dtype = filename[:-4]
#     df['dtype'] = dtype
#     df.to_csv(f'./wmo_climate_normals/{dtype}_mod.csv')



# dfs = []
# for filename in os.listdir('./wmo_climate_normals/mod'):
#     df = pd.read_csv('./wmo_climate_normals/mod/'+filename)
#     dfs.append(df)

# all_data = pd.concat(dfs)
# all_data.to_csv('./wmo_climate_normals/mod/all_data.csv')

#melt_wmo_data('./wmo_climate_normals/mod/', 'all_data_concat.csv', cols)

# df = pd.read_csv('./wmo_climate_normals/mod/all_data_concat_melted.csv')
# df['datatype'] = df['dtype'] + ' ' + df['Statistic Description']
# df.to_csv('./wmo_climate_normals/mod/all_data_concat_melted_mod.csv')


def calculate_total_daylength_for_month(latitude, month):
    #month = month_series.iloc[0]
    #latitude = latitude.iloc[0]
    months_days = {'Jan': (1, 31), 'Feb': (32, 59), 'Mar': (60, 90), 'Apr': (91, 121), 'May': (121, 151), 'Jun': (152, 181), 'Jul': (182, 212), 'Aug': (213, 243), 'Sep': (244, 273), 'Oct': (274, 304), 'Nov': (305, 334), 'Dec': (335, 365), 'Annual': (1, 365), 'Annual NCDC Computed Value': (1, 365)}
    days = months_days[month]
    total_dl = 0
    print(f'latitude is {latitude}, days of month are {days}')
    for day in range(days[0], days[1]+1):
        total_dl += daylength(day, latitude)
    print(total_dl)
    return total_dl


#add percent_possible_sunshine_column
def add_pps_column():
    sql = 'SELECT * FROM climate_normals JOIN iwmos ON iwmos.iwmo_id = climate_normals.iwmo'
    df = pd.read_sql(sql, conn)
    #df['total_daytime_length'] = df.apply(calculate_total_daylength_for_month(df['latitude'], df['month']), axis=1, result_type='broadcast') 
    df['total_daytime_length'] = df.apply(lambda row: calculate_total_daylength_for_month(row.latitude, row.month), axis=1)
    #df['total_daytime_length'] = calculate_total_daylength_for_month(df['latitude'], df['month'])
    df['percent_possible_sunshine'] = df['sunshine_mean_number_of_hours'] / df['total_daytime_length']

    df_climate = df[['id', 'iwmo', 'month', 'mean_temp_mean_value', 'mean_max_temp_mean_value', 'mean_min_temp_mean_value', 'humidity_mean_value', 'precipitation_data_mean_monthly_value', 'total_daytime_length', 'sunshine_mean_number_of_hours', 'percent_possible_sunshine']]
    df_climate.to_csv('./data/climate_data_with_pps.csv')
    #df_climate.to_sql('climate_normals', con=engine, if_exists='replace', index_label='id')

#pivot_wmo_data(filepath='./wmo_climate_normals/mod/', filename='all_data_concat_melted_mod.csv')

add_pps_column()