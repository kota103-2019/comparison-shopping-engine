# -*- coding: utf-8 -*-
import scrapy, datetime

from webcrawler.items import ProductItem

class TokopediaSpider(scrapy.Spider):
    name = 'tokopedia'
    allowed_domains = ['www.tokopedia.com']
    start_urls = [
        'https://www.tokopedia.com/p/kategori-komputer-aksesoris?ob=9&identifier=komputer-aksesoris&page=1'
        ]

    def parse(self, response):
        products = response.css("div._33JN2R1i div._27sG_y4O")
        for product_detail in products:
            product_link = product_detail.css("a::attr(href)").get()
            yield scrapy.Request(url=product_link, callback=self.parse_product)

        next_page_object = response.css("a.GUHElpkt::attr(href)").get()
        if(next_page_object is not None):
            next_page = str(next_page_object)
            next_page = 'https://www.tokopedia.com' + next_page
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_product(self, response):
        product_object = ProductItem()
        product_object['online_marketplace'] = self.name
        product_object['time_taken'] = datetime.datetime.now()
        product_object['url'] = response.url
        product_object['title'] = response.css("h1.rvm-product-title span::text").get()
        product_object['image_url'] = response.css("div.product-detail__img-holder div.content-img img::attr(src)").get()
        product_object['price_final'] = response.css("div.rvm-price-holder div.rvm-price input::attr(value)").get()
        product_object['rating'] = response.css("div.rate-accuracy div.reviewsummary-rating-score::text").get()
        product_object['condition'] = response.css("div.rvm-product-info div.rvm-product-info--item_value::text").get(1)
        product_object['seller'] = response.css("div.rvm-merchat-name span.shop-name::text").get()
        product_object['seller_url'] = response.css("div.rvm-merchat-name a::attr(href)").get()
        product_object['seller_location'] = response.css("div.rvm-merchat-city span::text").get()
        # product_object['category'] = response
        product_object['description'] = response.css("div#info").get()

        yield product_object