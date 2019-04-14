# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    currency = scrapy.Field()
    price = scrapy.Field()
    # seller_username = scrapy.Field()
    # seller_link = scrapy.Field()
    # seller_city = scrapy.Field()
    # feedback_summary = scrapy.Field()
    # feedback_link = scrapy.Field()
