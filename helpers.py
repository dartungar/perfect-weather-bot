from climate_dicts import mean_max_temp_range_dict, sunshine_percent_range_dict, precipitation_monthly_range_dict, mean_humidity_range_dict
import db
from db import conn, select, iwmos, c_normals, places
from places import get_nearby_locations_constraints, get_locations_by_constraints
from sqlalchemy import * 
import random


# TODO: точные критерии - как мы определяем "солнечный", "дождливый"? как выбираем данные примерно подходящие?
# например словарь соответствий: "тепло" - от 15 до 20
# или давать возможность выбирать сегменты самому
# TODO: не только функция "покажи все где больше или нет", но и "покажи где меньше или нет" - возможно в виде флага
# TODO: конверсия схожих параметров
def select_iwmos_by_weather(month='Jan', 
                            mean_temp_mean_range=(-10000,99999), 
                            mean_max_temp_mean_range=(-10000, 99999),
                            humidity_mean_range=(-10000,99999),
                            precipitation_monthly_range=(-10000,99999),
                            sunshine_percent_range=(-10000,99999)):
    sel = select([c_normals, iwmos]).where(and_(c_normals.c.iwmo == iwmos.c.iwmo_id, 
                                                c_normals.c.month == month,
                                                c_normals.c.mean_temp_mean_value.between(mean_temp_mean_range[0], mean_temp_mean_range[1]),
                                                c_normals.c.mean_max_temp_mean_value.between(mean_max_temp_mean_range[0], mean_max_temp_mean_range[1]),
                                                c_normals.c.humidity_mean_value.between(humidity_mean_range[0], humidity_mean_range[1]),
                                                c_normals.c.precipitation_data_mean_monthly_value.between(precipitation_monthly_range[0], precipitation_monthly_range[1]),
                                                c_normals.c.percent_possible_sunshine.between(sunshine_percent_range[0], sunshine_percent_range[1])
                                                ))

    result = conn.execute(sel)
    return result.fetchall()


# функция для получения погодных станций на основе словаря климатов. типа "солнечно" итд
def get_iwmos_by_climate_dict(month='Jan', mean_max_temp='none', humidity='none', precipitation_monthly='none', percent_sunshine='none'):
    mean_max_temp_range = mean_max_temp_range_dict[mean_max_temp]
    humidity_range = mean_humidity_range_dict[humidity]
    precipitation_monthly_range = precipitation_monthly_range_dict[precipitation_monthly]
    sunshine_range = sunshine_percent_range_dict[percent_sunshine]
    #logger.info('running select by range...')
    iwmos = select_iwmos_by_weather(month=month, 
                                    mean_max_temp_mean_range=mean_max_temp_range, 
                                    humidity_mean_range=humidity_range,
                                    precipitation_monthly_range=precipitation_monthly_range,
                                    sunshine_percent_range=sunshine_range)
    
    return iwmos


def get_nearby_locations_by_iwmo(iwmo, radius):
    iwmo_lat = iwmo[13]
    iwmo_long = iwmo[14]
    constraints = get_nearby_locations_constraints(iwmo_lat, iwmo_long, radius)
    locations = get_locations_by_constraints(iwmo_lat, iwmo_long, constraints)
    return locations





if __name__ == '__main__':

    iwmos = get_iwmos_by_climate_dict(month='Jan', mean_max_temp='freezing', sunshine_percent='sunny')

    print(len(iwmos))
    iwmo = random.choice(iwmos)
    #print(iwmo)
    print(f'{iwmo[10].strip()}, {iwmo[11].strip()} (https://www.google.com/maps/?q={iwmo[12]},{iwmo[13]})')


