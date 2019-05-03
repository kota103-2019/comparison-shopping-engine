# -*- coding: utf-8 -*-
import scrapy


class JdIdSpider(scrapy.Spider):
    name = 'jd.id'
    allowed_domains = ['www.jd.id']
    start_urls = [
        'http://www.jd.id/'
        ]

    def parse(self, response):
        pass
