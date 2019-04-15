# -*- coding: utf-8 -*-
import scrapy

from webcrawler.items import ProductItem

class BukalapakSpider(scrapy.Spider):
    name = 'bukalapak'
    allowed_domains = ['www.bukalapak.com']
    start_urls = ['https://www.bukalapak.com/c/komputer/laptop?page=1']

    def parse(self, response):
        product_links = response.css('div.basic-products ul.products li.col-12--2 article.product-display div.product-description')
        for product_detail in product_links:
            product_links = 'https://www.bukalapak.com' + product_detail.css('a::attr(href)').get()
            # yield{
            #     'product_title' : product_detail.css('a::attr(title)').get(),
            #     'product_link': 'https://www.bukalapak.com' + product_detail.css('a::attr(href)').get(),
            #     'currency' : product_detail.css('div.product-price span.currency::text').get(),
            #     'price' : product_detail.css('div.product-price span.amount::text').get(),
            #     'seller_username' : product_detail.css('div.product-seller h5.user__name a::text').get(),
            #     'seller_link' : 'https://www.bukalapak.com' + product_detail.css('div.product-seller h5.user__name a::attr(href)').get(),
            #     'seller_city' : product_detail.css('div.product-seller span.user-city__txt::text').get(),
            #     'feedback_summary' : product_detail.css('div.product-seller a.user-feedback-summary::text').get(),
            #     'feedback_link' : 'https://www.bukalapak.com' + product_detail.css('div.product-seller a.user-feedback-summary::attr(href)').get(),
            # }
            yield response.follow(product_links, callback=self.parse_product)

        next_page_object = response.css('a.next_page::attr(href)').get()
        if(next_page_object is not None):
            next_page = str(next_page_object)
            next_page = 'https://www.bukalapak.com' + next_page
            yield response.follow(next_page, callback=self.parse)
    
    def parse_product(self, response):
        product_object = ProductItem()
        product_object['url'] = response.url
        product_object['title'] = response.css('h1.c-product-detail__name::text').get()
        product_object['price'] = response.css('span.c-product-detail-price__installment span.amount::text').get()

        yield product_object
