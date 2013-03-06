import random
import datetime

def random_dates(begin, end, num):
    delta = end - begin
    delta_list = random.sample(xrange(delta.days), num) 
    return [end - datetime.timedelta(days=day) for day in delta_list]
    