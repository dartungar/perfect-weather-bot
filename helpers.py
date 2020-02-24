from climate_dicts import mean_temp_range_dict, sunshine_hours_range_dict, precipitation_monthly_range_dict, mean_humidity_range_dict
import db
from db import conn, select, iwmos, w_normals
from sqlalchemy import * 
import random


# TODO: точные критерии - как мы определяем "солнечный", "дождливый"? как выбираем данные примерно подходящие?
# например словарь соответствий: "тепло" - от 15 до 20
# или давать возможность выбирать сегменты самому
# TODO: не только функция "покажи все где больше или нет", но и "покажи где меньше или нет" - возможно в виде флага
# TODO: конверсия схожих параметров
def select_iwmos_by_weather(month='Jan', 
                            mean_temp_mean_range=(-10000,99999), 
                            humidity_mean_range=(-10000,99999),
                            precipitation_monthly_range=(-10000,99999),
                            sunshine_hours_range=(-10000,99999)):
    
    sel = select([w_normals, iwmos]).where(and_(w_normals.c.iwmo == iwmos.c.iwmo_id, 
                                                w_normals.c.month == month,
                                                w_normals.c.mean_temp_mean_value.between(mean_temp_mean_range[0], mean_temp_mean_range[1]),
                                                w_normals.c.humidity_mean_value.between(humidity_mean_range[0], humidity_mean_range[1]),
                                                w_normals.c.precipitation_data_mean_monthly_value.between(precipitation_monthly_range[0], precipitation_monthly_range[1]),
                                                w_normals.c.sunshine_mean_number_of_hours.between(sunshine_hours_range[0], sunshine_hours_range[1])
                                                ))

    result = conn.execute(sel)
    
    return result.fetchall()


# функция для получения погодных станций на основе словаря климатов. типа "солнечно" итд
def get_iwmos_by_climate_dict(month='Jan', mean_temp='none', humidity='none', precipitation_monthly='none', sunshine='none'):
    mean_temp_range = mean_temp_range_dict[mean_temp]
    humidity_range = mean_humidity_range_dict[humidity]
    precipitation_monthly_range = precipitation_monthly_range_dict[precipitation_monthly]
    sunshine_range = sunshine_hours_range_dict[sunshine]
    #logger.info('running select by range...')
    iwmos = select_iwmos_by_weather(month=month, 
                                    mean_temp_mean_range=mean_temp_range, 
                                    humidity_mean_range=humidity_range,
                                    precipitation_monthly_range=precipitation_monthly_range,
                                    sunshine_hours_range=sunshine_range)
    
    
    return iwmos


if __name__ == '__main__':

    iwmos = get_iwmos_by_climate_dict(month='Jan', mean_temp='freezing', sunshine='sunny')

    print(len(iwmos))
    iwmo = random.choice(iwmos)
    #print(iwmo)
    print(f'{iwmo[10].strip()}, {iwmo[11].strip()}')


