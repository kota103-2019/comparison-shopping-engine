# -*- coding: utf-8 -*-
# TODO : 
# []Location
# []Category
# []Discount 
# []Price_Original 
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
        #follow each product links
        for product_detail in products:
            product_link = product_detail.css("a::attr(href)").get()
            yield scrapy.Request(url=product_link, callback=self.parse_product, meta={
                'splash':{
                    'args':{
                        'html':1,
                        'wait':1,
                        # 'proxy':'http://10.10.0.6:3128',
                    },

                    'endpoint':'render.html',
                }
            })

        #go to the next page
        next_page = response.css("a.GUHElpkt::attr(href)").get()
        if(next_page is not None):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_product(self, response):
        product_object = ProductItem()
        product_object['online_marketplace'] = self.name
        product_object['time_taken'] = datetime.datetime.now()
        product_object['url'] = response.url
        
        #title and image url in string format
        product_object['title'] = response.css("h1.rvm-product-title span::text").get()
        product_object['image_url'] = response.css("div.product-detail__img-holder div.content-img img::attr(src)").get()
        
        #get price data in string '1234567'
        price = response.css("div.rvm-price-holder div.rvm-price input::attr(value)").get()
        #convert into float format
        product_object['price_final'] = float(price)
        
        #stock data are not found
        #replace with 'Informasi Stok Barang tidak Ditemukan'
        product_object['stock'] = 'Informasi Stok Barang tidak Ditemukan'

        #discount ? cashback ? 

        #get rating data in string '5.0'
        rating = response.css("div.rate-accuracy div.reviewsummary-rating-score::text").get()
        if rating is not None:
            #convert into float format
            product_object['rating'] = float(rating)
        
        #get condition data in string 'Baru' / 'Bekas'
        condition = response.css("div.rvm-product-info div.rvm-product-info--item_value::text").getall()[0]
        #check condition status
        #'Baru' = new_product
        if condition == 'Baru': new_product = 1 
        else: new_product = 0
        product_object['condition'] = new_product
        
        #seller and seller url in string format
        product_object['seller'] = response.css("div.rvm-merchat-name span.shop-name::text").get()
        product_object['seller_url'] = response.css("div.rvm-merchat-name a::attr(href)").get()
        
        #get seller location data in string format
        #convert into defined location data from location data in marketplace
        product_object['seller_location'] = response.css("div.pdp-shop__info p.pdp-shop__info__stats span::text").getall()[0]
        
        #get seller last activity in string format
        product_object['last_activity'] = response.css("div.pdp-shop__info p.pdp-shop__info__stats span::text").getall()[1]

        #convert into defined category data from start url 
        # product_object['category'] = response
        
        #description in string HTML format
        product_object['description'] = response.css("div#info").get()

        yield product_object