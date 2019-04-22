# -*- coding: utf-8 -*-
import scrapy, datetime

from webcrawler.items import ProductItem

class TokopediaSpider(scrapy.Spider):
    name = 'tokopedia'
    allowed_domains = ['www.tokopedia.com']
    start_urls = [
        'https://www.tokopedia.com/p/kategori-komputer-aksesoris'
        ]

    def parse(self, response):
        products = response.css("div._33JN2R1i div._27sG_y4O")
        for product_detail in products:
            product_link = product_detail.css("a::attr(href)").get()
            yield response.follow(product_link, callback=self.parse_product)

    def parse_product(self, response):
        product_object = ProductItem()
        product_object['time_taken'] = datetime.datetime.now()
        product_object['url'] = response.url
        product_object['title'] = response.css("h1.rvm-product-title span::text").get()
        product_object['price_final'] = response.css("div.rvm-price-holder div.rvm-price input::attr(value)").get()

        yield product_object