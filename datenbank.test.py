import datenbank
import configparser

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    datenbank.mysql_connect(host=config['database']['host'], port=config['database']['port'],
                            database=config['database']['database'], user=config['database']['user'],
                            password=config['database']['password'])
    datenbank.mysql_select_test()
    datenbank.mysql_insert_lister('hrtk', 'Hans', 'AGENCY')
    print(datenbank.mysql_select_lister('hrtk'))
    datenbank.mysql_insert_listing(listing_id=5127, listing_title='Hello', listing_description='iwruhwriouhj',
                         listing_availableFrom='2022-06-06', listing_offerType='rent', listing_deleted=1,
                         listing_deletedAt='2022-06-06', listing_createdAt='2022-06-06', listing_updatedAt='2022-06-06',
                         listing_address_street='Paradeplatz', listing_address_country='CH',
                         listing_address_postalCode=8634, listing_address_locality='Kirchberg',
                         listing_address_region='ZH', listing_geo='48.19976, 16.45572', listing_price_currency='CHF',
                         listing_price_rent_gross=3200, listing_price_rent_interval='monthly',
                         listing_price_buy_gross=400000, listing_price_buy_extra=2100, listing_numberOfRooms=5,
                         listing_livingSpace=142, lister_id='hrtk')
    datenbank.mysql_disconnect()
