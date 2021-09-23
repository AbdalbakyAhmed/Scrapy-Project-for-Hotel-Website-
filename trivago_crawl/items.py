# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TrivagoCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    hotel_name = scrapy.Field()
    hotel_link = scrapy.Field()
    image_link = scrapy.Field()
    rating = scrapy.Field()
    num_of_ratings = scrapy.Field()
    num_of_stars = scrapy.Field()
    distance_to_city_center = scrapy.Field()
    hotel_address = scrapy.Field()
    major_total_price = scrapy.Field()
    major_price_per_night = scrapy.Field()
    major_seller = scrapy.Field()
    minor_total_price = scrapy.Field()
    minor_price_per_night = scrapy.Field()
    minor_seller = scrapy.Field()
    lowest_price_per_night = scrapy.Field()
    lowest_seller = scrapy.Field()