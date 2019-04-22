# -*- coding: utf-8 -*-
import scrapy


class ShopeeSpider(scrapy.Spider):
    name = 'shopee'
    allowed_domains = ['www.shopee.com']
    start_urls = [
        'http://www.shopee.com/'
        ]

    def parse(self, response):
        pass
