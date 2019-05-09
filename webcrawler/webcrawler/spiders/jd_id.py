# -*- coding: utf-8 -*-
import scrapy, datetime

from webcrawler.items import ProductItem

class JdIdSpider(scrapy.Spider):
    name = 'jd.id'
    allowed_domains = ['www.jd.id']
    start_urls = [
        'https://www.jd.id/category/jual-pc-875061492.html'
        ]

    def parse(self, response):
        products = response.css('div.item div.p-desc')
        for product_detail in products:
            product_link = response.urljoin(product_detail.css('a::attr(href)').get())
            yield scrapy.Request(url=product_link, callback=self.parse_product)
        
        next_page_object = response.urljoin(response.css('div.pagination a.p-next::attr(href)').get())
        if(next_page_object is not None):
            next_page = str(next_page_object)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_product(self, response):
        product_object = ProductItem()
        product_object['online_marketplace'] = self.name
        product_object['time_taken'] = datetime.datetime.now()
        product_object['url'] = response.url
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