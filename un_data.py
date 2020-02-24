import csv
import os
import pandas as pd
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *


Base = declarative_base()
#engine = create_engine(os.environ['DATABASE_URL_WEATHER']) 
engine = create_engine('postgresql://postgres:Dfcbktr1@localhost:5432/weather')


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

pivot_wmo_data(filepath='./wmo_climate_normals/mod/', filename='all_data_concat_melted_mod.csv')