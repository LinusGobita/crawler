import logging
import crawler
import os
from datetime import datetime


offert_types = ["mieten", "kaufen"]


def get_things_from_one_listing(id, offert_typ = "mieten"):

    list_of_things = crawler.get_things_list_from_json()
    listing = crawler.get_listing_from_href(f"/{offert_typ}/{str(id)}")


    for thing in list_of_things:
        crawler.get_thing_from_listing(listing, thing)

    crawler.print_things_from_one_listing(list_of_things)




def get_all_listing_from_ch():
    counter = 0

    list_of_things = crawler.get_things_list_from_json()
    all_zip = crawler.get_all_ch_zip()

    for offert_type in offert_types:
        logging.info(f"Start with crawler in {offert_type}______________________________")

        for zip in all_zip:
            all_hrefs_from_one_plz = crawler.grab_all_hrefs_from_plz(zip, offert_type)


            for href in all_hrefs_from_one_plz:
                counter += 1
                crawler.take_a_break(f"Downloade Nr:\t{counter}\t(zip:{zip}{href})")

                #Get all data from Homegate to all_data_from_one_listing
                all_data_from_one_listing = crawler.get_listing_from_href(href)


                #Value wied dem thing zugewiesen
                for thing in list_of_things:
                    crawler.get_thing_from_listing(all_data_from_one_listing, thing)

                #Ausgane von listing in der Konsole
                crawler.print_things_from_one_listing(list_of_things)






def start_logging():
    counter = 0

    #Things for Logging
    log_file_path = "./logs"
    date_str = datetime.now().strftime("%Y%m%d")
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)

    log_file = os.path.join(log_file_path, f'logs_{date_str}.log')
    logging.basicConfig(
        level=logging.DEBUG,
        filename=log_file,
        filemode="a+",
        format="%(asctime)-15s %(message)s"
    )