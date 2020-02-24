from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *
import os
import netCDF4
import numpy as numpy
from netCDF4 import Dataset
#from psycopg2.extensions import register_adapter, AsIS

Base = declarative_base()
engine = create_engine(os.environ['DATABASE_URL_WEATHER']) 
DBSession = sessionmaker(bind=engine)
session = DBSession()


# def adapt_numpy_float32(numpy_float32):
#     return AsIS(numpy_float32)


# register_adapter(numpy.float32, adapt_numpy_float32)


class ColumbianData(Base):
    __tablename__ = 'columbian_data'
    id = Column(Integer, primary_key=True)
    iwmo_index = Column(Integer)
    month = Column(Float)
    climate_mean_temp = Column(Float)
    mean_temp = Column(Float)
    mean_max_temp = Column(Float)
    mean_min_temp = Column(Float)
    mean_sunshine = Column(Float)
    sunshine_count = Column(Float)
    total_precipitation = Column(Float)


class Iwmo(Base):
    __tablename__ = 'iwmos'
    id = Column(Integer, primary_key=True)
    iwmo_id = Column(String)
    name = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)


def build_historical_data(session):
    for i in range(0, 10494):
        for t in range(0, 215):
            hist_data = ColumbianData(
                            iwmo_index=i,
                            month=times[t].item(),
                            climate_mean_temp=climate_mean_temps[i, t].item(),
                            mean_temp=mean_temps[i, t].item(),
                            mean_max_temp=mean_max_temps[i, t].item(),
                            mean_min_temp=mean_min_temps[i, t].item(),
                            mean_sunshine=mean_sunshines[i, t].item(),
                            sunshine_count=sunshine_counts[i, t].item(),
                            total_precipitation=total_precip[i, t].item()
            )
            session.add(hist_data)
            
            if t == 0:
                session.commit()
                print(f'starting data on iwmo {i}...')


def build_iwmo_list(session):
    for i in range(0, 10494):
        iwmo = Iwmo(
                iwmo_id = ''.join(chr(j) for j in iwmos[i] if j > 0),
                name = ''.join(chr(k) for k in names[i]),
                country = ''.join(chr(l) for l in countries[i]),
                latitude = lats[i].item(),
                longitude = lons[i].item(),
                elevation = elevs[i].item()
        )  
        session.add(iwmo)
        session.commit()
        print(f'starting iwmo {i}...')


if not engine.dialect.has_table(engine, 'iwmos'):
    Base.metadata.create_all(engine)

if not engine.dialect.has_table(engine, 'columbian_data'):
    Base.metadata.create_all(engine)


if __name__ == '__main__':

    path_to_dataset = 'data.nc'
    data = Dataset(path_to_dataset, format="NETCDF4")

    iwmos = numpy.ma.filled(data.variables['IWMO'])
    names = numpy.ma.filled(data.variables['Name'])
    countries = numpy.ma.filled(data.variables['Country'])
    lats = numpy.ma.filled(data.variables['lat'])
    lons = numpy.ma.filled(data.variables['lon'])
    elevs = numpy.ma.filled(data.variables['elev'])
    times = numpy.ma.filled(data.variables['T'])
    climate_mean_temps = numpy.ma.filled(data.variables['DATA.climate.mean.temp'])
    mean_temps = numpy.ma.filled(data.variables['DATA.mean.temp'])
    mean_max_temps = numpy.ma.filled(data.variables['DATA.mean.maximum.temp'])
    mean_min_temps = numpy.ma.filled(data.variables['DATA.mean.minimum.temp'])
    mean_sunshines = numpy.ma.filled(data.variables['DATA.mean.sunshine'])
    sunshine_counts = numpy.ma.filled(data.variables['DCNTS.daily.sunshine.count'])
    total_precip = numpy.ma.filled(data.variables['DATA.climate.total.prcp'])

    build_historical_data(session)
    #build_iwmo_list(session)