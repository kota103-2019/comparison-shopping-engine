# -*- coding: utf-8 -*-
import scrapy

from webcrawler.items import ProductItem


class BukalapakSpider(scrapy.Spider):
    name = 'bukalapak'
    # allowed_domains = ['https://www.bukalapak.com/c/komputer/laptop']
    start_urls = ['https://www.bukalapak.com/c/komputer/laptop?page=1']

    def parse(self, response):
        # print('current page : ' + response.url)
        product_links = response.css('div.basic-products ul.products li.col-12--2 article.product-display div.product-description')
        for product_detail in product_links:
            product_object = ProductItem()
            product_object['title'] = product_detail.css('a::attr(title)').get()
            product_object['url'] = 'https://www.bukalapak.com' + product_detail.css('a::attr(href)').get()
            product_object['currency'] = product_detail.css('div.product-price span.currency::text').get()
            product_object['price'] = product_detail.css('div.product-price span.amount::text').get()
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
            yield product_object

        next_page_object = response.css('a.next_page::attr(href)').get()
        if(next_page_object is not None):
            next_page = str(next_page_object)
            page_num = next_page.split('?page=')
            next_page = 'https://www.bukalapak.com' + next_page
            # if int(page_num[1]) <= 2:
            # print('next page : ' + next_page)
            yield response.follow(next_page, callback=self.parse)
