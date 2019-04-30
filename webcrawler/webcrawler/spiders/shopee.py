# -*- coding: utf-8 -*-
import scrapy


class ShopeeSpider(scrapy.Spider):
    name = 'shopee'
    allowed_domains = ['www.shopee.com']
    start_urls = [
        'https://shopee.co.id/Komputer-Aksesoris-cat.134?page=0&sortBy=ctime'
        ]

    def parse(self, response):
        pass