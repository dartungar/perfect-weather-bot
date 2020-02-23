from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *


Base = declarative_base()
metadata = Base.metadata
#engine = create_engine(os.environ['DATABASE_URL_WEATHER']) 
engine = create_engine('postgresql://postgres:Dfcbktr1@localhost:5432/weather')

conn = engine.connect()

w_normals = Table('climate_normals', metadata,
                    Column('iwmo', String),
                    Column('month', String),
                    Column('humidity_mean_value', Float),
                    Column('mean_max_temp_mean_value', Float),
                    Column('mean_min_temp_mean_value', Float),
                    Column('mean_temp_mean_value', Float),
                    Column('mean_temp_median_value', Float),
                    Column('precipitation_data_mean_monthly_value', Float),
                    Column('precipitation_data_median_value', Float),
                    Column('sunshine_mean_daily_value', Float),
                    Column('sunshine_mean_number_of_hours', Float),
                    Column('sunshine_percent_of_possible', Float),
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


# test_weather_select = select([w_normals, iwmos]).where(and_(w_normals.c.iwmo == iwmos.c.iwmo_id, w_normals.c.sunshine_percent_of_possible < 5))

# result = conn.execute(test_weather_select)
# print(result.fetchone())