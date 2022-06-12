import logging

from prettytable import PrettyTable

import crawler
import os
from datetime import datetime

import tools

offert_types = ["mieten", "kaufen"]

def beispiel_SQL_ohne_klassen(id, offert_typ = "mieten"):
    list_of_things = crawler.get_things_list_from_json()
    listing = crawler.get_listing_from_href(f"/{offert_typ}/{str(id)}")


    for thing in list_of_things:
        crawler.get_thing_from_listing(listing, thing)


    ### Beispiel ohne Klassen
    dic_listing = dict()
    dic_lister = dict()


    for thing in list_of_things:
        if thing.sql_table == "listing":
            dic_listing[thing.typ] = thing.value

        elif thing.sql_table == "lister":
            dic_lister[thing.typ] = thing.value



    items_iterator = iter(dic_listing)
    first_item = next(items_iterator)
    secound_item = next(items_iterator)


    listing_values = dic_listing.values()
    values_interator = iter(listing_values)
    first_value = next(values_interator)
    secound_value = next(values_interator)

    print(f"INSERTa INTO listing({first_item}, {secound_item}) \n"
          f"VALUES ({first_value}, |||\n"
          f"{secound_value})")






def save_one_listing_to_txt(id, offert_typ = "mieten"):
    list_of_things = crawler.get_things_list_from_json()
    listing = crawler.get_listing_from_href(f"/{offert_typ}/{str(id)}")

    for thing in list_of_things:
        crawler.get_thing_from_listing(listing, thing)

    tools.save_to_txt(list_of_things)




def get_all_listing_from_ch():
    counter = 0


    list_of_things = crawler.get_things_list_from_json()
    all_zip = crawler.get_all_ch_zip()

    tools.start_logging()

    for offert_type in offert_types:
        logging.info(f"Start with crawler in {offert_type}______________________________")

        for zip in all_zip:
            all_hrefs_from_one_plz = crawler.grab_all_hrefs_from_plz(zip, offert_type)


            for href in all_hrefs_from_one_plz:
                counter += 1
                tools.take_a_break(f"Downloade Nr:\t{counter}\t(zip:{zip}{href})")

                #Get all data from Homegate to all_data_from_one_listing
                all_data_from_one_listing = crawler.get_listing_from_href(href)

                #Der Crawler wird gestartet
                for thing in list_of_things:
                    crawler.get_thing_from_listing(all_data_from_one_listing, thing)





                listing_as_obj = crawler.from_data_to_obj(list_of_things)











                # Beispiel mit Klassen
                table_listing = PrettyTable(['listing', 'value'])

                table_listing.add_row(["id", listing_as_obj.listing_id])
                table_listing.add_row(["postalCode", listing_as_obj.listing_address_postalCode])
                table_listing.add_row(["offer type", listing_as_obj.listing_offerType])
                table_listing.add_row(["street", listing_as_obj.listing_address_street])
                table_listing.add_row(["img", listing_as_obj.listing_img_url])

                print(table_listing)
