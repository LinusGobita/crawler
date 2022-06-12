import mariadb
import sys

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


def mysql_insert_lister(lister_id, lister_name, lister_type):
    cur.execute(f"INSERT INTO lister (lister_id, lister_name, lister_type) VALUES"
                f"('{lister_id}', '{lister_name}', '{lister_type}')")


def mysql_select_lister(lister_id):
    cur.execute(f"SELECT * FROM lister WHERE lister_id = '{lister_id}'")
    return cur.fetchall()


def mysql_insert_listing(listing_id, listing_title, listing_description, listing_availableFrom, listing_offerType,
                         listing_deleted, listing_deletedAt, listing_createdAt, listing_updatedAt,
                         listing_address_street, listing_address_country, listing_address_postalCode,
                         listing_address_locality, listing_address_region, listing_geo, listing_price_currency,
                         listing_price_rent_gross, listing_price_rent_interval, listing_price_buy_gross,
                         listing_price_buy_extra, listing_numberOfRooms, listing_livingSpace, lister_id):
    lister_check = mysql_select_lister(lister_id=lister_id)
    if len(lister_check) != 1:
        print(f"ERROR: Lister '{lister_id}' not found!")
        sys.exit(1)
    cmd = f"INSERT INTO listing (listing_id, listing_title, listing_description, listing_availableFrom, " \
          f"listing_offerType, listing_deleted, listing_deletedAt, listing_createdAt, listing_updatedAt," \
                f"listing_address_street, listing_address_country, listing_address_postalCode, " \
                f"listing_address_locality, listing_address_region, listing_geo, listing_price_currency," \
                f"listing_price_rent_gross, listing_price_rent_interval, listing_price_buy_gross," \
                f"listing_price_buy_extra, listing_numberOfRooms, listing_livingSpace, lister_id)" \
                f"VALUES ({listing_id}, '{listing_title}', '{listing_description}', '{listing_availableFrom}'," \
                f"'{listing_offerType}', {listing_deleted}, '{listing_deletedAt}', '{listing_createdAt}'," \
                f"'{listing_updatedAt}', '{listing_address_street}', '{listing_address_country}'," \
                f"{listing_address_postalCode}, '{listing_address_locality}', '{listing_address_region}', " \
                f"POINT({listing_geo}), '{listing_price_currency}', {listing_price_rent_gross}," \
                f"'{listing_price_rent_interval}', {listing_price_buy_gross}, {listing_price_buy_extra}," \
                f" {listing_numberOfRooms}, {listing_livingSpace}, '{lister_id}')"
    print(cmd)
    cur.execute(cmd)


def mysql_select_listing(listing_id):
    cur.execute(f"SELECT * FROM listing WHERE listing_id = '{listing_id}'")
    return cur.fetchall()


def mysql_insert_listingCategory(listing_id, listingCategory_name):
    listing_check = mysql_select_listing(listing_id=listing_id)
    if len(listing_check) != 1:
        print(f"ERROR: Listing '{listing_check}' not found!")
        sys.exit(1)
    cur.execute(f"INSERT INTO listingCategory (listing_id, listingCategory_name) VALUES"
                f"('{listing_id}', '{listingCategory_name}')")


def mysql_insert_listingPlatform(listing_id, listingPlatform_name):
    listing_check = mysql_select_listing(listing_id=listing_id)
    if len(listing_check) != 1:
        print(f"ERROR: Listing '{listing_check}' not found!")
        sys.exit(1)
    cur.execute(f"INSERT INTO listingPlatform_name (listing_id, listingPlatform_name) VALUES"
                f"('{listing_id}', '{listingPlatform_name}')")


if __name__ == "__main__":
    print("This file should not be run directly")
    sys.exit(1)

