import database


def save_things_into_db(list_of_things):
    listing_id = ""
    lister_id = ""

    listing_categories = []
    listing_typ = ""
    listing_value = ""
    lister_typ = ""
    lister_value = ""

    for thing in list_of_things:

        # Wenn es das Letzte Element im Array ist
        element = ", "
        if thing == list_of_things[-1]:
            element = ") "

        #special forces
        if thing.sql_row == "str":
            thing.value = "'"+str(thing.value)+"'"
        elif thing.typ == "listing_categories":
            listing_categories = thing.value

        #Normal table
        if thing.sql_table == "listing":
            listing_typ = listing_typ + thing.typ + element
            listing_value = listing_value + str(thing.value) + element
            if thing.typ == "listing_id":
                listing_id = thing.value

        elif thing.sql_table == "lister":
            lister_typ = lister_typ + thing.typ + element
            lister_value = lister_value + str(thing.value) + element
            if thing.typ == "lister_id":
                lister_id = thing.value

    database.save_to_one_table("listing_id", listing_id, "listing", listing_typ, listing_value)
    database.save_to_one_table("lister_id", lister_id, "lister", lister_typ, lister_value)
    print("Listing Categories = " + listing_categories)



