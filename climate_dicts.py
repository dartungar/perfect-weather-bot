
# mean_temp_range_dict = {'scorching': (30, 100),
#                     'hot': (24, 30),
#                     'warm': (18, 24),
#                     'temperate': (12, 18),
#                     'tepid': (6, 12),
#                     'cold': (-6, 6),
#                     'freezing': (-80, -6),
#                     'none': (-10000, 10000)}

mean_max_temp_range_dict = {'scorching': (30, 100),
                    'hot': (24, 30),
                    'warm': (18, 24),
                    'temperate': (12, 18),
                    'tepid': (5, 12),
                    'cold': (-6, 5),
                    'freezing': (-80, -6),
                    'none': (-10000, 10000)}

mean_min_temp_range_dict = {'none': (-10000, 10000)
                            }

mean_humidity_range_dict = {'none': (-10000, 10000)
                            }

precipitation_monthly_range_dict = {'none': (-10000, 10000),
                                    'constantly': (130, 10000),
                                    'often': (85, 130),
                                    'sometimes': (50, 85),
                                    'rarely': (20, 50),
                                    'very rarely': (0, 20) 
                            }


sunshine_hours_range_dict = {'very sunny': (180, 10000),
                    'sunny': (100, 180),
                    'normal': (50, 100),
                    'cloudy': (20, 50),
                    'very cloudy': (0, 20),
                    'none': (-10000, 10000)}

sunshine_percent_range_dict = {'very sunny': (0.75, 1.5),
                    'sunny': (0.55, 0.75),
                    'normal': (0.33, 0.55),
                    'cloudy': (0.15, 0.33),
                    'very cloudy': (0, 0.15),
                    'none': (-10000, 10000)}


months_translate_dict = {'Jan': 'Jan',
                         'Feb': 'Feb',
                         'Mar': 'Mar',
                         'Apr': 'Apr',
                         'May': 'May',
                         'Jun': 'Jun',
                         'Jul': 'Jul',
                         'Aug': 'Aug',
                         'Sep': 'Sep',
                         'Oct': 'Oct',
                         'Nov': 'Nov',
                         'Dec': 'Dec',
                         'Янв': 'Jan',
                         'Фев': 'Feb',
                         'Мар': 'Mar',
                         'Апр': 'Apr',
                         'Май': 'May',
                         'Июн': 'Jun',
                         'Июл': 'Jul',
                         'Авг': 'Aug',
                         'Сен': 'Sep',
                         'Окт': 'Oct',
                         'Ноя': 'Nov',
                         'Дек': 'Дек'}

temperature_translate_dict = {'scorching': 'scorching',
                    'hot': 'hot',
                    'warm': 'warm',
                    'temperate': 'temperate',
                    'tepid': 'tepid',
                    'cold': 'cold',
                    'freezing': 'freezing',
                    'skip': 'none',
                    'обжигающе': 'scorching',
                    'жарко': 'hot',
                    'тепло': 'warm',
                    'умеренно': 'temperate',
                    'прохладно': 'tepid',
                    'холодно': 'cold',
                    'морозно': 'freezing',
                    'всё равно': 'none'}

precipitation_translate_dict = {'skip': 'none',
                                'constantly': 'constantly',
                                'often': 'often',
                                'sometimes': 'sometimes',
                                'rarely': 'rarely',
                                'very rarely': 'very rarely',
                                'всё равно': 'none',
                                'постоянно': 'constantly',
                                'часто': 'often',
                                'периодически': 'sometimes',
                                'редко': 'rarely',
                                'очень редко': 'very rarely'
}

sunshine_translate_dict = {'very sunny': 'very sunny',
                        'sunny': 'sunny',
                        'normal': 'normal',
                        'cloudy': 'cloudy',
                        'very cloudy': 'very cloudy',
                        'skip': 'none',
                        'очень солнечно': 'very sunny',
                        'солнечно': 'sunny',
                        'нормально': 'normal',
                        'облачно': 'cloudy',
                        'очень облачно': 'very cloudy',
                        'всё равно': 'none'
}