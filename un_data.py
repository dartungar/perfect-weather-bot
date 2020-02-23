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
    df = df.drop(columns=['Statistic Description', 'Unit', 'dtype', 'Country or Territory', 'Station Name', 'WMO Station Number'])
    df['Datatype'] = df['Datatype'].str.replace(' ', '_')
    df['Datatype'] = df['Datatype'].str.lower()
    df = df.rename(columns={'IWMO': 'iwmo', 'Month': 'month'})
    df_pivoted = pd.pivot_table(df, index=['iwmo', 'month'], columns=['Datatype'], values='Value', fill_value=-9999.0)
    #df_pivoted.to_csv('./wmo_climate_normals/mod/all_data_concat_melted_mod_pivoted.csv')
    df_pivoted.to_sql('climate_normals', con=engine)


#melt_wmo_data('sunshine.csv')

cols = ['dtype', 
        'WMO Station Number', 
        'Country or Territory', 
        'Station Name',  
        'Statistic Description', 
        'Unit', 
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 
        'Annual', 'Annual NCDC Computed Value']

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