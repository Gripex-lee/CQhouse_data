# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseDataItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    price_per = scrapy.Field()
    price_total = scrapy.Field()
    room_number = scrapy.Field()
    living_room_number = scrapy.Field() 
    high = scrapy.Field() 
    house_toward = scrapy.Field()   
    house_type = scrapy.Field() 
    size = scrapy.Field()
    build_year = scrapy.Field()
    buding_type = scrapy.Field()
    dianti = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()


    # wuye_price = scrapy.Field()
    # green_rate = scrapy.Field()
    # car_position = scrapy.Field()
    # rongji_rate = scrapy.Field()
