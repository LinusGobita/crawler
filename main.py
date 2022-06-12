from datetime import datetime
import logging
import os

import crawler
import datenbank
import iCrawler

if __name__ == "__main__":

    #Logging Yes Or No
#    iCrawler.start_logging()


    #Get One Listing
    iCrawler.get_things_from_one_listing(3001912432)

    crawler.get_listing_from_href("/href/3001912432")


    #Get All Listingd
#    iCrawler.get_all_listing_from_ch()



