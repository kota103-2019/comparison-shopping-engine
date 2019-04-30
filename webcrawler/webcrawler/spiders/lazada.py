# -*- coding: utf-8 -*-
import scrapy


class LazadaSpider(scrapy.Spider):
    name = 'lazada'
    allowed_domains = ['www.lazada.com']
    start_urls = [
        'https://www.lazada.co.id/beli-laptop/?page=1&spm=a2o4j.home.cate_1.2.1dea4ceeVhW9Zw'
        ]

    def parse(self, response):
        pass
