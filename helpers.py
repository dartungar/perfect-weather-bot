import db
from db import conn, select, iwmos, w_normals
import random
from sqlalchemy import * 

# TODO: точные критерии - как мы определяем "солнечный", "дождливый"? как выбираем данные примерно подходящие?
# например словарь соответствий: "тепло" - от 15 до 20
# или давать возможность выбирать сегменты самому
# TODO: не только функция "покажи все где больше или нет", но и "покажи где меньше или нет" - возможно в виде флага
# TODO: конверсия схожих параметров
def select_iwmos_by_weather(month='Jan', 
                            mean_temp_mean_range=(-10000,99999), 
                            mean_temp_median_range=(-10000,99999),
                            mean_max_temp_mean_range=(-10000,99999),
                            mean_min_temp_mean_range=(-10000,99999),
                            humidity_mean_range=(-10000,99999),
                            precipitation_monthly_range=(-10000,99999),
                            sunshine_hours_range=(-10000,99999),
                            sunshine_percent_range=(-10000,99999)):
    
    sel = select([w_normals, iwmos]).where(and_(w_normals.c.iwmo == iwmos.c.iwmo_id, 
                                                w_normals.c.month == month,
                                                w_normals.c.mean_temp_mean_value.between(mean_temp_mean_range[0], mean_temp_mean_range[1]),
                                                w_normals.c.mean_temp_median_value.between(mean_temp_median_range[0], mean_temp_median_range[1]),
                                                w_normals.c.mean_max_temp_mean_value.between(mean_max_temp_mean_range[0], mean_max_temp_mean_range[1]),
                                                w_normals.c.mean_min_temp_mean_value.between(mean_min_temp_mean_range[0], mean_min_temp_mean_range[1]),
                                                w_normals.c.humidity_mean_value.between(humidity_mean_range[0], humidity_mean_range[1]),
                                                w_normals.c.precipitation_data_mean_monthly_value.between(precipitation_monthly_range[0], precipitation_monthly_range[1]),
                                                w_normals.c.sunshine_mean_number_of_hours.between(sunshine_hours_range[0], sunshine_hours_range[1]),
                                                w_normals.c.sunshine_percent_of_possible.between(sunshine_percent_range[0], sunshine_percent_range[1])
                                                ))

    result = conn.execute(sel)
    
    return result.fetchall()


# функция для получения погодных станций на основе словаря климатов. типа "солнечно" итд
def get_iwmos_by_climate_dict(weather_dict, mean_temp='', humidity='', precipitation_monthly='', sunshine=''):
    mean_temp_range =
    humidity_range = 
    precipitation_monthly_range =
    sunshine_range = 

    iwmos = select_iwmos_by_weather(month='Feb', 
                                    mean_temp_mean_range=mean_temp_range, 
                                    humidity_mean_range=humidity_range,
                                    precipitation_monthly_range=precipitation_monthly_range,
                                    sunshine_hours_range=sunshine_range)
    return iwmos




















# iwmos = select_iwmos_by_weather(month='Feb', mean_temp_mean_range=(10, 20), sunshine_hours_range=(180, 400), humidity_mean_range=(30, 90))

# print(len(iwmos))
# for iwmo in iwmos:
#     print(f'{iwmo[14].strip()}, {iwmo[15].strip()}')