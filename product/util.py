import datetime
import random
import time

"""
    @author shibbir
    shibbirhssn@gmail.com
"""

def generate_scan_id(user_id):
    timestamp = time.time()

    generated_scan_id = str(user_id)+'-'+datetime.datetime.fromtimestamp(timestamp).strftime('%Y%m%d%H%M%S')
    return generated_scan_id


def generate_rating_id(user_id):
    timestamp = time.time()

    generated_rating_id = str(user_id) + '-' + datetime.datetime.fromtimestamp(timestamp).strftime('%Y%m%d%H%M%S')
    return generated_rating_id

def generate_random_arrayfill():
    random_number_list = []
    for i in range(0,2513):
        random_number = generate_random_number(0, 2000)
        rand_json = {
            i : random_number
        }
        random_number_list.append(rand_json)

    print(random_number_list)

    return random_number_list



def generate_random_number(start_val, end_val):

    random_number = random.randint(start_val, end_val)
    return random_number
