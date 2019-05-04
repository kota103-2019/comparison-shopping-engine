# -*- coding: utf-8 -*-
import scrapy

from webcrawler.items import ProductItem

class LazadaSpider(scrapy.Spider):
    name = 'lazada'
    
    def start_requests(self):
        urls = [
            'https://www.lazada.co.id/beli-laptop/?page=1&spm=a2o4j.home.cate_1.2.1dea4ceeVhW9Zw'
        ]
        for url_item in urls:
            yield scrapy.Request(url=url_item, callback=self.parse, meta={
                'splash':{
                    'args':{
                        'html':1,
                    }
                }
            })

    def parse(self, response):
        products = response.css("div.c2prKC div.c3KeDq div.c16H9d")
        for product_detail in products:
            product_link = response.urljoin(product_detail.css("a::attr(href)").get())
            yield scrapy.Request(url=product_link, callback=self.parse_product, meta={
                'splash':{
                    'args':{
                        'html':1,
                    }
                }
            })

    def parse_product(self, response):
        yield{
            'url' : response.url
        }