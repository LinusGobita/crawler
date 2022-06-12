import datetime
from enum import Enum


class ListingType(Enum):
    RENT = "RENT"
    BUY = "BUY"


class Listing:

    def __init__(self, listing_id: int, listing_title: str, listing_description: str,
                 listing_availableFrom: datetime.date, listing_offerType: ListingType,
                 listing_createdAt: datetime.datetime, listing_updatedAt: datetime.datetime,
                 listing_address_street: str, listing_address_country: str, listing_address_postalCode: int,
                 listing_address_locality: str, listing_address_region: str, listing_geo_x: float, listing_geo_y: float,
                 listing_price_currency: str, listing_price_rent_gross: float, listing_price_rent_interval: str,
                 listing_price_buy_gross: float, listing_price_buy_extra: float, listing_numberOfRooms: float,
                 listing_livingSpace: float, lister_id: str):
        self.listing_id = listing_id
        self.listing_title = listing_title
        self.listing_description = listing_description
        self.listing_availableFrom = listing_availableFrom
        if listing_offerType not in ListingType:
            print(f"ERROR: OfferType '{listing_offerType} not known!")
            exit(1)
        self.listing_offerType = listing_offerType.value
        self.listing_createdAt = listing_createdAt
        self.listing_updatedAt = listing_updatedAt
        self.listing_address_street = listing_address_street
        self.listing_address_country = listing_address_country
        self.listing_address_postalCode = listing_address_postalCode
        self.listing_address_locality = listing_address_locality
        self.listing_address_region = listing_address_region
        self.listing_geo_x = listing_geo_x
        self.listing_geo_y = listing_geo_y
        self.listing_price_currency = listing_price_currency
        self.listing_price_rent_gross = listing_price_rent_gross
        self.listing_price_rent_interval = listing_price_rent_interval
        self.listing_price_buy_gross = listing_price_buy_gross
        self.listing_price_buy_extra = listing_price_buy_extra
        self.listing_numberOfRooms = listing_numberOfRooms
        self.listing_livingSpace = listing_livingSpace
        self.lister_id = lister_id
