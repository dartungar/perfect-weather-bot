
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

# 250+ солнечно, 200-250 весьма солнечно, 100-200 нормально, 50-100 облачно, 0-50 ваще пиздос
sunshine_hours_range_dict = {'very sunny': (180, 10000),
                    'sunny': (100, 180),
                    'normal': (50, 100),
                    'cloudy': (20, 50),
                    'very cloudy': (0, 20),
                    'none': (-10000, 10000)}
