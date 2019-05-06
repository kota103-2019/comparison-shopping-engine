# -*- coding: utf-8 -*-
import scrapy


class ShopeeSpider(scrapy.Spider):
    name = 'shopee'

    def start_requests(self):
        urls = [
            'https://shopee.co.id/Komputer-Aksesoris-cat.134?page=0&sortBy=ctime'
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
        pass

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