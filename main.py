import crawler
import iCrawler
import tools

if __name__ == "__main__":

    iCrawler.get_listing_categories_between_ids_as_txt(3001920200)
    iCrawler.save_listings_between_ids_to_txt(3001925486)
    iCrawler.save_json_to_export(3001925486)
    iCrawler.save_listings_between_ids_to_txt(3001925495)
    iCrawler.save_one_listing_to_database(3001886756)
#    iCrawler.get_all_listing_from_ch()



