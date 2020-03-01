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

c_normals = Table('climate_normals', metadata,
                    Column('iwmo', String),
                    Column('month', String),
                    Column('humidity_mean_value', Float),
                    Column('mean_max_temp_mean_value', Float),
                    Column('mean_min_temp_mean_value', Float),
                    Column('mean_temp_mean_value', Float),
                    Column('precipitation_data_mean_monthly_value', Float),
                    Column('sunshine_mean_number_of_hours', Float),
                    )


iwmos = Table('iwmos', metadata,
                Column('id', Integer),
                Column('iwmo_id', String),
                Column('name', String),
                Column('country', String),
                Column('latitude', Float),
                Column('longitude', Float),
                Column('elevation', Float),
                )


places = Table('places', metadata,
                Column('id', Integer),
                Column('country_code', String),
                Column('city', String),
                Column('accent_city', String),
                Column('region', String),
                Column('population', String),
                Column('latitude', Float),
                Column('longitude', Float),
                )