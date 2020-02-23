import csv 
import netCDF4
import numpy as numpy
from netCDF4 import Dataset

data = Dataset("data.nc", format="NETCDF4")



iwmos = data.variables['IWMO']
names = data.variables['Name']
countries = data.variables['Country']
lats = data.variables['lat']
lons = data.variables['lon']
elevs = data.variables['elev']
times = data.variables['T']
climate_mean_temps = data.variables['DATA.climate.mean.temp']
mean_temps = data.variables['DATA.mean.temp']
mean_max_temps = data.variables['DATA.mean.maximum.temp']
mean_min_temps = data.variables['DATA.mean.minimum.temp']
mean_sunshines = data.variables['DATA.mean.sunshine']
sunshine_counts = data.variables['DCNTS.daily.sunshine.count']
total_precip = data.variables['DATA.climate.total.prcp']

fieldnames = ['iwmo', 
                #'name', 
                #'country', 
                #'latitude', 
                #'longitude', 
                #'elevation', 
                't', 
                'climate_mean_temp', 
                'mean_temp', 
                'mean_max_temp', 
                'mean_min_temp', 
                'mean_sunshine', 
                'sunshine_count', 
                'total_precipitation']

with open('test_data2.csv', mode='w') as test_data:
    #test_writer = csv.writer(test_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    dict_writer = csv.DictWriter(test_data, extrasaction='ignore', fieldnames=fieldnames)
    dict_writer.writeheader()



    for i in range(0, 10494):
        for t in range (0, 215):
            #iwmo = ''.join(chr(j) for j in iwmos[i] if j > 0)
            #name = ''.join(chr(k) for k in names[i])
            #country = ''.join(chr(l) for l in countries[i])

            data = {
                'iwmo': i, #сделаем отдельную таблицу для станций, с названиями итд. тут слишком медленно по-моему это считать
                #'name': name, 
                #'country': country, 
                #'latitude': lats[i], 
                #'longitude': lons[i], 
                #'elevation': elevs[i], 
                't': times[t], 
                'climate_mean_temp': climate_mean_temps[i, t], 
                'mean_temp': mean_temps[i, t], 
                'mean_max_temp': mean_max_temps[i, t], 
                'mean_min_temp': mean_min_temps[i, t], 
                'mean_sunshine': mean_sunshines[i, t], 
                'sunshine_count': sunshine_counts[i, t], 
                'total_precipitation': total_precip[i, t]
            }
            #data = [iwmo, name, times[t], lats[i], lons[i], elevs[i], country, climate_mean_temps[i, t], mean_temps[i, t], mean_max_temps[i, t], mean_min_temps[i, t], mean_sunshines[i, t], sunshine_counts[i, t], total_precip[i, t]]
            #data = [iwmos[i, t], times[t]]

            dict_writer.writerow(data)

            if t == 0:
                print(f'started iwmo {i}')
            #print(f'row {i} x {t}')
