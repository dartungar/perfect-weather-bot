from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *
import pandas as pd
import os


Base = declarative_base()
metadata = Base.metadata
engine = create_engine(os.environ['DATABASE_URL_WEATHER']) 
#engine = create_engine('postgresql://postgres:Dfcbktr1@localhost:5432/weather')

conn = engine.connect()


def build_db():
    df_climate_normals = pd.read_csv('./data/climate_data_with_pps.csv')
    df_climate_normals = df_climate_normals[['iwmo', 'month', 'mean_temp_mean_value', 'mean_max_temp_mean_value', 'mean_min_temp_mean_value', 'humidity_mean_value', 'precipitation_data_mean_monthly_value', 'sunshine_mean_number_of_hours', 'percent_possible_sunshine']]
    df_climate_normals.to_sql('climate_normals', con=engine, if_exists='replace', index_label='id', dtype={'iwmo': String()})

    df_iwmos = pd.read_csv('./data/iwmos.csv', index_col='index')
    df_iwmos = df_iwmos.drop(columns=['id'])
    df_iwmos.to_sql('iwmos', con=engine, if_exists='replace', index_label='id', dtype={'iwmo_id': String()})


def build_places_db():
    for i in range(0, 3300000, 100000):
        print(f'building places in range {i} to db...')
        df_places = pd.read_csv(f'./data/places_{i+100000}.csv', index_col='id')
        df_places.to_sql('places', con=engine, if_exists='append', dtype={'region': String()})


if __name__ == '__main__':

    build_db()
    #build_places_db() # quite lengthy process due to the need to separate long .csv into ~30 shorter .csv due to 1GB RAM server limitations
    
    # index on lat and long values to speed up the search
    add_index_sql = f'''CREATE INDEX coordinates_index ON places(latitude, longitude)'''

    conn.execute(add_index_sql)