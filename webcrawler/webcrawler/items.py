# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    time_taken = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    price_final = scrapy.Field()    
    price_original = scrapy.Field()
    price_installment = scrapy.Field()
    discount = scrapy.Field()
    rating = scrapy.Field()
    kondisi = scrapy.Field()
    seller = scrapy.Field()
    seller_url = scrapy.Field()
    seller_location = scrapy.Field()