# -*- coding: utf-8 -*-
#[]Location
#[]Category
#[]Seller Information
#   has separate scraper
#[]Seller Name
#[]Seller Location
#[]Seller Url
#[]Seller Last Activity

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
                        # 'proxy':'http://10.10.0.6:3128',
                    },

                    'endpoint':'render.html',
                }
            })

    def parse(self, response):
        products = response.css("div.c2prKC div.c3KeDq div.c16H9d")
        #follow each product links
        for product_detail in products:
            product_link = response.urljoin(product_detail.css("a::attr(href)").get())
            yield scrapy.Request(url=product_link, callback=self.parse_product)
        
        # next_page_object = response

    def parse_product(self, response):
        product_object = ProductItem()
        product_object['online_marketplace'] = self.name
        product_object['time_taken'] = datetime.datetime.now()
        product_object['url'] = response.url
        
        #title and image url in string format
        product_object['title'] = response.css("div.pdp-product-title span.pdp-mod-product-badge-title::text").get()
        product_object['image_url'] = response.urljoin(response.css("div.gallery-preview-panel__content img.gallery-preview-panel__image::attr(src)").get())
        
        #get price data in string '1234567'
        price = response.css("div.pdp-mod-product-price div.pdp-product-price span.pdp-price::text").get()
        #cleaning up data, deleting 'Rp' and '.'
        price = price.replace('Rp','').replace('.','')
        #convert into float format
        product_object['price_final'] = float(price)
        
        #stock data are not found
        #replace with 'Informasi Stok Barang tidak Ditemukan'
        product_object['stock'] = 'Informasi Stok Barang tidak Ditemukan'
        
        #check discount
        is_discount = response.css('div.pdp-mod-product-price div.pdp-product-price div.origin-block span.pdp-price::text').get() is not None
        if(is_discount):
            #get price data in string '1234567'
            price_original = response.css('div.pdp-mod-product-price div.pdp-product-price div.origin-block span.pdp-price::text').get()
            #cleaning up data, deleteting 'Rp' and '.'
            price_original = price_original.replace('Rp','').replace('.','')
            #convert into float format
            product_object['price_original'] = float(price_original)

            #get discount data in string '-1%'
            discount = response.css("div.pdp-mod-product-price div.pdp-product-price div.origin-block span.pdp-product-price__discount::text").get()
            #cleaning up data, deleting '%' and '-'
            discount = discount.replace('%','').replace('-','')
            #convert into float format '1.0'
            product_object['discount'] = float(discount)

        #get rating data in string '5.0'
        rating = response.css("div.summary span.score-average::text").get()
        if rating is not None:
            #convert into float format
            product_object['rating'] = float(rating)
        
        #assumed product condition is new => 'Baru' = new_product
        new_product = 1
        product_object['condition'] = new_product
        
        #seller and seller url in string format
        # product_object['seller'] = response.css("div.seller-name div.seller-name__detail a.seller-name__detail-name::text").get()
        # product_object['seller_url'] = response.urljoin(response.css("div.seller-name div.seller-name__detail a.seller-name__detail-name::attr(href)").get())
        
        #get seller location data in string format
        #convert into defined location data from location data in marketplace
        # product_object['seller_location'] = response

        #get seller last activity in string format
        # product_object['last_activity'] = 
        
        #convert into defined category data from start url 
        # product_object['category'] = response
        
        #description in string HTML format
        # product_object['description'] = response
        
        yield product_object