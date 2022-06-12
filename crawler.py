import json
import logging
import os
import random
import pandas as pd
import time

import requests
from bs4 import BeautifulSoup


############ Get URLs ############
from prettytable import PrettyTable

base_url = "https://www.homegate.ch"

class Thing:
    def __init__(self, typ, jsonReader, sql_table, sql_row, value=0,):
        self.typ = typ
        self.jsonReader = jsonReader
        self.sql_table = sql_table
        self.sql_row = sql_row
        self.value = value

def take_a_break(infos):
    #Timer
    sleep_min = 1
    sleep_max = 5
    sleeptimes = list(range(sleep_min, sleep_max, 1))
    t = random.choice(sleeptimes)

    while t != 0:
        print(f"Take a Coffe for {t} secounts", end=' ')
        time.sleep(1)
        print(end='\r')
        t -= 1
    print(f'{infos}')

def get_things_list_from_json():
    list_of_things = []
    try:
        with open("./things.json") as f:
            data = json.load(f)
            for item in data:
                typ = item
                value = data[typ]
                json_Reader = value[0]
                sql = value[1]
                sql_table = sql[0]
                sql_row = sql[1]
                thing = Thing(typ, json_Reader, sql_table, sql_row)
                list_of_things.append(thing)

    except Exception as err:
        logging.error(err)

    return list_of_things


def grab_all_hrefs_from_ch_with_offertType(offerType):
    href_list_ch = []


    zip_in_ch = get_all_ch_zip()

    for zip in zip_in_ch:
        take_a_break(f"next zip will be = {zip} ")
        href_list_ch.append(grab_all_hrefs_from_plz(zip, offerType))

    return href_list_ch

def grab_all_hrefs_from_plz(zip, offerType):

    #Queck the Input
    art = ["kaufen", "mieten"]
    if str(offerType).lower() not in art:
        logging.error("falsche eingabe! Bitte mieten oder kaufen eingeben")
        return

    #Vatiablen
    href_list = []
    page = 0
    #print(url_offert)

    while True:
        page += 1
        url_offert = base_url + "/" + str(offerType) + '/immobilien/plz-' + str(zip) + "/trefferliste?ep=" + str(page)

        try:
            response = requests.get(url_offert)
            soup = BeautifulSoup(response.text, "html.parser")
            listingsGroup = BeautifulSoup(str(soup.find("div", {"data-test": "result-list"})), "html.parser")
            listingsList = listingsGroup.find_all("a", {"data-test": "result-list-item"})
        except Exception as err:
            logging.error(f"err by url. {url_offert}", err)

        for listing in listingsList:
            #print(f'page :{page} grab Advertisement {listing["href"]} ')
            href_list.append(listing["href"])

        if page > 50:
            break
        if len(listingsList) < 10:
            print(f'\nzip: {zip} has {page} page and {len(href_list)} inserat')
            break
    return href_list

############ Get Data ############
def get_all_ch_zip():

    plz_flie = pd.read_csv('./Postleitzahlen-Schweiz.csv', header=None)
    plz_flie.head()
    zip_in_ch = plz_flie[0]

    return zip_in_ch

def get_json_from_href(href):

    url = base_url + href

    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html.parser')

    except Exception as err:
        logging.error(f"err by url: {url} ", err)

    for script in soup.find_all('script'):
        the_hole_json = script.text.split('window.__INITIAL_STATE__=')

        if len(the_hole_json) > 1:
            try:
                dataNotFormatet = json.loads(the_hole_json[1].split('__INITIAL_STATE__=')[0])
                return dataNotFormatet

            except Exception as e:
                logging.warning(e)

def get_listing_from_href(href):
    js = get_json_from_href(href)
    js2 = js["listing"]
    return js2["listing"]

def get_thing_from_listing(listing, thing):
    try:
        leng = len(thing.jsonReader)

        if leng == 1:
            thing.value = listing[thing.jsonReader[0]]
        elif leng == 2:
            thing.value = listing[thing.jsonReader[0]][thing.jsonReader[1]]
        elif leng == 3:
            thing.value = listing[thing.jsonReader[0]][thing.jsonReader[1]][thing.jsonReader[2]]
        elif leng == 4:
            thing.value = listing[thing.jsonReader[0]][thing.jsonReader[1]][thing.jsonReader[2]][thing.jsonReader[3]]
        elif leng == 5:
            thing.value = listing[thing.jsonReader[0]][thing.jsonReader[1]][thing.jsonReader[2]][thing.jsonReader[3]][thing.jsonReader[4]]

    except Exception as err:
        logging.info(f"Datentyp {err} nicht gefunden {thing.value}")


def print_things_from_one_listing(things):



    table_listing = PrettyTable(['listing', 'value'])
    table_lister = PrettyTable(['lister', 'value'])

    for thing in things:

        if thing.sql_table == "listing":
            table_listing.add_row([thing.typ, thing.value])

        elif thing.sql_table == "lister":
            table_lister.add_row([thing.typ, thing.value])



    print(table_listing)
    print(table_lister)




############ Get Data  Deep impact############
class Characheristic:
    def __init__(self, typ, value):
        self.typ = typ
        self.value = value



def get_listing_info_from_listing(listing):
    localization = listing["localization"]
    de = localization["de"]
    text = de["text"]
    title = text["title"]
    description = text["description"]
    offerType = listing["offerType"]
    deleted = listing["deleted"]
    id = listing["id"]
    categories = listing["categories"]

    address = listing["address"]
    street = address["street"]
    postalCode = address["postalCode"]
    locality = address["locality"]
    region = address["region"]

    geoCoordinates = address["geoCoordinates"]
    latitude = geoCoordinates["latitude"]
    longitude = geoCoordinates["longitude"]

    attachments = de["attachments"]
    url_images = []
    for attachment in attachments:
        if attachment["type"] == "IMAGE":
            url_images.append(attachment["url"])

    if listing["offerType"] == "BUY":
        prices = listing["prices"]
        currency = prices["currency"]

        buy = prices["buy"]
        area = buy["area"]
        price_buy = buy["price"]
    elif listing["offerType"] == "RENT":
        prices = listing["prices"]
        currency = prices["currency"]

        rent = prices["rent"]
        interval = rent["interval"]
        gross = rent["gross"]

def get_lister_from_listing(listing):
    lister = listing["lister"]
    phone = lister["phone"]
    website = lister["website"]
    id = lister["id"]
    type = lister["type"]

def get_characheristics_from_listing(listing):
    all_characheristics_in_list = []
    characheristics = listing["characteristics"]

    for item in characheristics:
        characheristic = item
        value = characheristics[characheristic]
        characheristic = Characheristic(characheristic, value)
        all_characheristics_in_list.append(characheristic)

def get_title(listing):
    print(listing)
    title = listing["localization"]["de"]["text"]["title"]
    print(title)
    return title

