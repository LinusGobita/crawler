import datenbank
import configparser
from classes.Lister import Lister, ListerType
from classes.Listing2 import Listing, ListingType

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    datenbank.mysql_connect(host=config['database']['host'], port=config['database']['port'],
                            database=config['database']['database'], user=config['database']['user'],
                            password=config['database']['password'])
    print("DB Connect OK")
    datenbank.mysql_select_test()
    print("DB SELECT Test OK")
    lister = Lister(lister_id="hrtk", lister_name="Hans", lister_type=ListerType.AGENCY)
    datenbank.mysql_insert_lister(lister)
    print("DB INSERT Lister OK")
    print(datenbank.mysql_select_lister('hrtk'))
    print("DB SELECT Lister OK")
    listing = Listing(listing_id=5127, listing_title='Hello', listing_description='iwruhwriouhj',
                      listing_availableFrom='2022-06-06', listing_offerType=ListingType.RENT,
                      listing_createdAt='2022-06-06', listing_updatedAt='2022-06-06',
                      listing_address_street='Paradeplatz', listing_address_country='CH',
                      listing_address_postalCode=8634, listing_address_locality='Kirchberg',
                      listing_address_region='ZH', listing_geo_x=48.19976, listing_geo_y=16.45572,
                      listing_price_currency='CHF', listing_price_rent_gross=3200,
                      listing_price_rent_interval='monthly', listing_price_buy_gross=400000,
                      listing_price_buy_extra=2100, listing_numberOfRooms=5, listing_livingSpace=142, lister_id='hrtk')
    datenbank.mysql_insert_listing(listing)
    print("DB INSERT Listing OK")
    datenbank.mysql_disconnect()
    print("DB Disconnect OK")
