import configparser
import datetime
import logging
import os
import datetime
import time
import random

from prettytable import PrettyTable

def start_logging():
    counter = 0

    #Things for Logging
    log_file_path = "./logs"
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)

    log_file = os.path.join(log_file_path, f'logs_{date_str}.log')
    logging.basicConfig(
        level=logging.DEBUG,
        filename=log_file,
        filemode="a+",
        format="%(asctime)-15s %(message)s"
    )

def save_to_txt(name, sting_1, string_2 = ""):
    file_path = "./export"
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    file = os.path.join(file_path, f"{name}.txt")
    with open(f"{file}", "w+") as f:
        f.write(str(sting_1))
        f.write("\n")
        f.write(str(string_2))




def things_from_one_listing_to_table(listing):
    #Benötigt die Things
    tables = []
    listing_id = "none"
    table_listing = PrettyTable(['listing', 'value'])
    table_lister = PrettyTable(['lister', 'value'])

    for thing in listing:
        if thing.typ == "listing_id":
            listing_id = thing.value

        #Nur die ersten Zeichen durchen
        first_char = str(thing.value)[0:40]
        if thing.sql_table == "listing":
            table_listing.add_row([thing.typ, first_char])

        elif thing.sql_table == "lister":
            table_lister.add_row([thing.typ, first_char])

    tables.append(listing_id)
    tables.append(table_listing)
    tables.append(table_lister)
    return tables




def take_a_break(sleep_min = 1, sleep_max = 5, infos = ""):
    #Timer
    sleeptimes = list(range(sleep_min, sleep_max, 1))
    t = random.choice(sleeptimes)

    while t != 0:
        print(f"Take a Coffe for {t} secounts", end=' ')
        time.sleep(1)
        print(end='\r')
        t -= 1
    print(f'{infos}')


def split_table_name_in_dic(list_of_things):
    listing_dic = dict()
    lister_dic = dict()

    for thing in list_of_things:
        if thing.sql_table == "listing":
            listing_dic[thing.typ] = thing.value
        elif thing.sql_table == "lister":
            lister_dic[thing.typ] = thing.value

    return listing_dic, lister_dic

def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config