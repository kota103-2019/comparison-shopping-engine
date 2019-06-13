# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    online_marketplace = scrapy.Field()
    time_taken = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    price_final = scrapy.Field()    
    price_original = scrapy.Field()
    # price_installment = scrapy.Field()
    stock = scrapy.Field()
    discount = scrapy.Field()
    rating = scrapy.Field()
    condition = scrapy.Field()
    seller = scrapy.Field()
    seller_url = scrapy.Field()
    seller_location = scrapy.Field()
    last_activity = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()