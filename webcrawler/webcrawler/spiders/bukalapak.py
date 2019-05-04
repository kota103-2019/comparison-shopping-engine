# -*- coding: utf-8 -*-
import scrapy, datetime

from webcrawler.items import ProductItem

class BukalapakSpider(scrapy.Spider):
    name = 'bukalapak'
    allowed_domains = ['www.bukalapak.com']
    start_urls = [
        "https://www.bukalapak.com/c/komputer?from=category_home&page=1&search%5Bkeywords%5D=",
        "https://www.bukalapak.com/c/perlengkapan-kantor?from=category_home&page=1&search%5Bkeywords%5D="
        ]

    def parse(self, response):
        products = response.css('div.basic-products ul.products li.col-12--2 article.product-display div.product-description')
        for product_detail in products:
            product_link = 'https://www.bukalapak.com' + product_detail.css('a::attr(href)').get()
            yield scrapy.Request(url=product_link, callback=self.parse_product)

        next_page_object = response.css('a.next_page::attr(href)').get()
        if(next_page_object is not None):
            next_page = str(next_page_object)
            next_page = 'https://www.bukalapak.com' + next_page
            yield scrapy.Request(url=next_page, callback=self.parse)
    
    def parse_product(self, response):
        product_object = ProductItem()
        product_object['online_marketplace'] = self.name
        product_object['time_taken'] = datetime.datetime.now()
        product_object['url'] = response.url
        product_object['title'] = response.css('h1.c-product-detail__name.qa-pd-name::text').get()
        product_object['image_url'] = response.css("div.c-product-image-gallery picture img::attr(src)").get()
        product_object['price_final'] = response.css('div.c-product-detail-price::attr(data-reduced-price)').get()
        is_installment = response.css('div.c-product-detail-price::attr(data-installment)').get() == 'true'
        is_discount = response.css('div.c-product-detail-price span.c-product-detail-price__original span.amount::text').get() is not None
        if(is_installment):
            product_object['price_installment'] = str(response.css('span.c-product-detail-price__installment span.amount::text').get()).replace(".","")
        if(is_discount):
            product_object['price_original'] = str(response.css('div.c-product-detail-price span.c-product-detail-price__original span.amount::text').get()).replace(".","")
        product_object['rating'] = response.css('span.c-product-rating__value.is-hidden::text').get()
        product_object['condition'] = response.css('dd.c-deflist__value.qa-pd-condition-value span.c-label::text').get()
        product_object['seller'] = response.css('a.c-user-identification__name.qa-seller-name::text').get()
        product_object['seller_url'] = 'https://www.bukalapak.com' + response.css('a.c-user-identification__name.qa-seller-name::attr(href)').get()
        product_object['seller_location'] = response.css("span.c-user-identification-location__txt.qa-seller-location a::text").get()
        product_object['category'] = str(response.css("dd.c-deflist__value.qa-pd-category-value.qa-pd-category::text").get()).replace("\n","")
        product_object['description'] = response.css("div.qa-pd-description p").get()

        yield product_object