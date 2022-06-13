import logging
import crawler
import iDatabase
import tools

offert_types = ["rent", "buy"]

def save_listings_between_ids_to_txt(id_1, id_2=0, offert_typ ="rent"):
    i = id_1
    if id_2 == 0:
        id_2 = i
    for i in range (id_1, id_2):
        table = tools.things_from_one_listing_to_table(crawler.return_one_listing_from_id(i, offert_typ))
        tools.save_to_export(table[0], table[1], table[2])
        tools.take_a_break(1, 3, f"Next ID wil be {i+1}")

def save_json_to_export(id, offert_typ = "rent"):
    list_of_things_with_value = crawler.get_listing_from_href(f"/{offert_typ}/{id}")
    tools.save_to_export(id, list_of_things_with_value, file="json")


def save_one_listing_to_database(id, offert_typ = "rent"):
    list_of_things_with_value = crawler.return_one_listing_from_id(id, offert_typ)
    iDatabase.save_things_into_db(list_of_things_with_value)



def save_all_listing_from_ch_in_database():
    counter = 0
    tools.start_logging()
    all_zip = crawler.get_all_ch_zip()

    for offert_type in offert_types:
        logging.info(f"Start with crawler in {offert_type}______________________________")

        for zip in all_zip:
            all_hrefs_from_one_plz = crawler.grab_all_hrefs_from_plz(zip, offert_type)

            for href in all_hrefs_from_one_plz:
                counter += 1
                tools.take_a_break(f"Downloade Nr:\t{counter}\t(zip:{zip}{href})")
                list_of_things_with_value = crawler.return_one_listing_from_href(href)
                iDatabase.save_things_into_db(list_of_things_with_value)



def get_listing_categories_between_ids_as_txt(id_1, id_2=0):
    all_categories = ['OPEN_SLOT', 'COMMERCIAL', 'DUPLEX', 'RETAIL',
                      'HOUSE', 'ATTIC_FLAT', 'UNDERGROUND_SLOT', 'HOBBY_ROOM',
                      'SHOP', 'PRACTICE', 'LOFT', 'APARTMENT', 'STUDIO', 'SINGLE_HOUSE',
                      'FURNISHED_FLAT', 'CHALET', 'COVERED_PARKING_PLACE_BIKE', 'VILLA', 'OFFICE',
                      'BACHELOR_FLAT', 'SINGLE_GARAGE', 'STORAGE_ROOM', 'ROOF_FLAT', 'FLAT']
    if id_2 == 0:
        id_2 = id_1
    i = id_1
    tools.start_logging()

    for i in range(id_1, id_2):
        all_things_in_data  = crawler.return_one_listing_from_id(i)
        for thing in all_things_in_data:
            if thing.typ == "listing_categories":
                if thing.value == None:
                    break
                for cat in thing.value:
                    all_categories.append(cat)
        tools.take_a_break(5, 10, f"ID NR = {i} found categories=: {str(list(set(all_categories)))}",)
        i += 1

    tools.save_to_export(f"categories_{id_1}-{id_2}", str(list(set(all_categories))))