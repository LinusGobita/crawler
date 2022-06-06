import os
from random import random
import pandas as pd
from time import sleep

import requests
from bs4 import BeautifulSoup

def get_all_ch_zip():

    plz_flie = pd.read_csv('./Postleitzahlen-Schweiz.csv', header=None)
    plz_flie.head()
    zip_in_ch = plz_flie[0]

    for zip in zip_in_ch:
        print(zip)


def grab_all_hrefs_from_ch(offerType):
    #Timer
    sleep_min = 1
    sleep_max = 5
    sleeptimes = list(range(sleep_min, sleep_max, 1))

def grab_all_hrefs_from_plz(plz, offerType):
    #"obj = mieten oder kaufen"

    base_url_rent = 'https://www.homegate.ch/mieten/immobilien/plz-'
    base_url_buy  = 'https://www.homegate.ch/kaufen/immobilien/plz-'

    link_list = []

    os.listdir()
    page = 0

    if str(offerType).lower() == "rent":
        url = base_url_rent + str(plz) + "/trefferliste"
    elif str(offerType).lower() == "buy":
        url = base_url_buy + str(plz) + "/trefferliste"


    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    listingsGroup = BeautifulSoup(str(soup.find("div", {"data-test": "result-list"})), "html.parser")
    listingsList = listingsGroup.find_all("a", {"data-test": "result-list-item"})

    for listing in listingsList:
        # print(f'page :{page} grab Advertisement {listing["href"]} ')
        link_list.append(listing["href"])

    for listening in link_list:
        print(listening)



if __name__ == "__main__":

#    grab_all_hrefs_from_plz(8048, "buy")

    get_all_ch_zip()