# -*- coding: utf-8 -*-
import scrapy, datetime

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
        
        # next_page_object = response

    def parse_product(self, response):
        product_object = ProductItem()
        product_object['online_marketplace'] = self.name
        product_object['time_taken'] = datetime.datetime.now()
        product_object['url'] = response.url
        product_object['title'] = response
        product_object['title'] = response
        product_object['image_url'] = response
        product_object['price_final'] = response
        product_object['rating'] = response
        product_object['condition'] = response
        product_object['seller'] = response
        product_object['seller_url'] = response
        product_object['seller_location'] = response
        product_object['category'] = response
        product_object['description'] = response
        
        yield product_object