from db import conn, select, iwmos, c_normals, places
from sqlalchemy import * 
import pandas as pd

def get_nearby_locations_constraints(lat, lon, distance_km):
    lat_constraint_min = lat - (distance_km / 111.139)
    lat_constraint_max = lat + (distance_km / 111.139)
    lon_constraint_min = lon - (distance_km / 111.139)
    lon_constraint_max = lon + (distance_km / 111.139)

    return ((lat_constraint_min, lat_constraint_max), (lon_constraint_min, lon_constraint_max))


def get_locations_by_constraints(lat, lon, constraints):
    lat_constraints = constraints[0]
    lon_constraints = constraints[1]

    sel = select([places]).where(and_(
                                        places.c.latitude.between(lat_constraints[0], lat_constraints[1]),
                                        places.c.longitude.between(lon_constraints[0], lon_constraints[1])
    ))

    result = conn.execute(sel)
    return result.fetchall()


country_codes = pd.read_csv('./data/country_codes.csv')
    