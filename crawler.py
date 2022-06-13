import json
import logging
import os

import pandas as pd

import tools
import requests
from bs4 import BeautifulSoup


############ Get URLs ############
from prettytable import PrettyTable

base_url = "https://www.homegate.ch"

class Thing:
    def __init__(self, typ, jsonReader, sql_table, datatype, value=None, ):
        self.typ = typ
        self.jsonReader = jsonReader
        self.sql_table = sql_table
        self.datatype = datatype
        self.value = value

def return_one_listing_from_id(id, offert_typ ="rent"):
    list_of_things = get_things_list_from_json()
    all_data_from_one_listing = get_listing_from_href(f"/{offert_typ}/{str(id)}")

    #Values Werden dem thing zugeordnet
    for thing in list_of_things:
        get_thing_from_listing(all_data_from_one_listing, thing)

    return list_of_things
def return_one_listing_from_href(href):
    list_of_things = get_things_list_from_json()
    all_data_from_one_listing = get_listing_from_href(href)

    # Values Werden dem thing zugeordnet
    for thing in list_of_things:
        get_thing_from_listing(all_data_from_one_listing, thing)

    return list_of_things

#Noch bischien auseinander nehmen!
def download_img(id, urls):
    counter = 0
    file_path = f"./export/img/{id}"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    for url in urls:
        if url["type"] == "IMAGE":
            file = os.path.join(file_path, f"{id}-{counter}")
            response = requests.get(url["url"])
            file = open(f"{file}.jpg", "wb")
            file.write(response.content)
            file.close()
            counter += 1


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
        tools.take_a_break(f"next zip will be = {zip} ")
        href_list_ch.append(grab_all_hrefs_from_plz(zip, offerType))

    return href_list_ch

def grab_all_hrefs_from_plz(zip, offerType):

    #Queck the Input
    art = ["rent", "buy"]
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
#        print(f"request on url = {url} is = {r}")
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
    status = queck_if_everithing_is_ok(js)
    if status == "err":
        print(f"somethig went rong with this listing {href}")
        return f"somethig went rong with this listing {href}"
    try:
        js2 = js["listing"]
        return js2["listing"]
    except Exception as e:
        logging.info(f"no info data found on {href} : {e}")

def queck_if_everithing_is_ok(json):

    try:
        status = json["listing"]["isLoading"]
        id = json["listing"]["dataFetchError"]["listingId"]
        message = json["listing"]["dataFetchError"]["message"]

        tools.save_to_export(f"error/{id}", str(json))
        logging.info(f"inserat with id {id} has the error massage: {message}")
        return "err"

    except Exception as e:
        return "ok"


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
        elif leng == 6:
                thing.value = listing[thing.jsonReader[0]][thing.jsonReader[1]][thing.jsonReader[2]][thing.jsonReader[3]][thing.jsonReader[4]][thing.jsonReader[5]]

    except Exception as err:
        logging.info(f"Datentyp {err} nicht gefunden {thing.value}")
