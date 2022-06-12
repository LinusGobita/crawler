import mariadb
import sys
from classes.Listing import Listing
from classes.Lister import Lister


def mysql_connect(host, port, database, user, password):
    global cur, conn
    try:
        conn = mariadb.connect(
            user=user,
            password=password,
            host=host,
            port=int(port),
            database=database
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        exit(1)
    cur = conn.cursor()


def mysql_disconnect():
    conn.commit()
    conn.close()


def mysql_select_test():
    cur.execute("SELECT listing_id, listing_title FROM listing")
    for (listing_id, listing_title) in cur:
        print(f"id: {listing_id}, title: {listing_title}")


def mysql_insert_lister(lister: Lister):
    if not isinstance(lister, Lister):
        print("ERROR: Invalid data")
        exit(1)
    cur.execute(f"CALL sp_insert_lister('{lister.lister_id}', '{lister.lister_name}', '{lister.lister_type}')")


def mysql_select_lister(lister_id):
    cur.execute(f"SELECT * FROM lister WHERE lister_id = '{lister_id}'")
    return cur.fetchall()


def mysql_insert_listing(listing: Listing):
    if not isinstance(listing, Listing):
        print("ERROR: Invalid data")
        exit(1)
    lister_check = mysql_select_lister(lister_id=listing.lister_id)
    if len(lister_check) != 1:
        print(f"ERROR: Lister '{listing.lister_id}' not found!")
        exit(1)
    cmd = f"CALL sp_insert_listing({listing.listing_id}, '{listing.listing_title}', '{listing.listing_description}'," \
          f" '{listing.listing_availableFrom}', '{listing.listing_offerType}', '{listing.listing_createdAt}'," \
          f" '{listing.listing_updatedAt}', '{listing.listing_address_street}', '{listing.listing_address_country}'," \
          f" {listing.listing_address_postalCode}, '{listing.listing_address_locality}'," \
          f" '{listing.listing_address_region}', {listing.listing_geo_x}, {listing.listing_geo_y}," \
          f" '{listing.listing_price_currency}', {listing.listing_price_rent_gross}," \
          f" '{listing.listing_price_rent_interval}', {listing.listing_price_buy_gross}," \
          f" {listing.listing_price_buy_extra}, {listing.listing_numberOfRooms}, {listing.listing_livingSpace}," \
          f" '{listing.lister_id}')"
    print(cmd)
    cur.execute(cmd)


def mysql_select_listing(listing_id):
    cur.execute(f"SELECT * FROM listing WHERE listing_id = '{listing_id}'")
    return cur.fetchall()


def mysql_insert_listingCategory(listing_id, listingCategory_name):
    listing_check = mysql_select_listing(listing_id=listing_id)
    if len(listing_check) != 1:
        print(f"ERROR: Listing '{listing_check}' not found!")
        exit(1)
    cur.execute(f"INSERT INTO listingCategory (listing_id, listingCategory_name) VALUES"
                f"('{listing_id}', '{listingCategory_name}')")


def mysql_insert_listingPlatform(listing_id, listingPlatform_name):
    listing_check = mysql_select_listing(listing_id=listing_id)
    if len(listing_check) != 1:
        print(f"ERROR: Listing '{listing_check}' not found!")
        exit(1)
    cur.execute(f"INSERT INTO listingPlatform_name (listing_id, listingPlatform_name) VALUES"
                f"('{listing_id}', '{listingPlatform_name}')")


if __name__ == "__main__":
    print("This file should not be run directly")
    sys.exit(1)
