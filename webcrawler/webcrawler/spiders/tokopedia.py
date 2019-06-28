# -*- coding: utf-8 -*-
# TODO : 
# []Location
# []Category
# []Discount 
# []Price_Original 
import scrapy, datetime, pymongo

from webcrawler.items import ProductItem

class TokopediaSpider(scrapy.Spider):
    name = 'tokopedia'
    
    def start_requests(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["comparison-shopping-engine"]
        kota_collection = db["kota"]

        urls = [
            # "https://www.tokopedia.com/p/komputer-aksesoris/desktop-mini-pc",
            # "https://www.tokopedia.com/p/laptop-aksesoris/laptop",
            "https://www.tokopedia.com/p/komputer-aksesoris/komponen-komputer/monitor",
        ]

        for url_item in urls:
            yield scrapy.Request(url=url_item, callback=self.parse, meta={
                "collection" : kota_collection
            })

    def parse(self, response):
        kota_collection = response.meta["collection"]

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
                },
                'collection' : kota_collection,
            })

        #go to the next page
        next_page = response.css("a.GUHElpkt::attr(href)").get()
        if(next_page is not None):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse, meta={
                "collection" : kota_collection
            })

    def parse_product(self, response):
        kota_collection = response.meta["collection"]

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

        #set original price with the same value as final price
        product_object['price_original'] = float(price)
        #set discount to 0.0
        product_object['discount'] = 'Informasi Discount tidak Ditemukan'
        #discount ? cashback ? 

        #set rating to 0.0
        product_object['rating'] = float(0)
        #get rating data in string '5.0'
        rating = response.css("div.rate-accuracy div.reviewsummary-rating-score::text").get()
        if rating is not None:
            #convert into float format
            product_object['rating'] = float(rating)
        
        #set condition status to 1, default is 1 "Baru"
        #'Baru' = new_product
        new_product = 1
        #get condition data in string 'Baru' / 'Bekas'
        condition = response.css("div.rvm-product-info div.rvm-product-info--item_value::text").getall()[0]
        #check condition status
        if condition == 'Bekas': new_product = 0
        product_object['condition'] = new_product
        
        #seller and seller url in string format
        product_object['seller'] = response.css("div.rvm-merchat-name span.shop-name::text").get()
        product_object['seller_url'] = response.css("div.rvm-merchat-name a::attr(href)").get()
        
        #get seller location data in string format
        #convert into defined location data from location data in marketplace
        location_string = response.css("div.pdp-shop__info p.pdp-shop__info__stats span::text").getall()[0]
        location_string = str(location_string).upper().replace("KAB.", "KABUPATEN")
        location_string = str(location_string).upper().replace("DKI JAKARTA", "JAKARTA PUSAT")
        #get "kota" data from database
        #then assing seller_location with "idkota"
        kota = kota_collection.find_one({"namaKota" : {"$regex" : ".*{}.*".format(location_string)}})
        idkota = ""
        if kota is not None:
            idkota = kota["idKota"]
        product_object['seller_location'] = idkota

        #get seller last activity in string format
        product_object['last_activity'] = response.css("div.pdp-shop__info p.pdp-shop__info__stats span::text").getall()[1]

        #convert into defined category data from start url     
        #'Dsktp' = Desktop
        #'Lptop' : Laptop
        #'Mntr' : Monitor
        product_object['category'] = 'Mntr'
        
        #description in string HTML format
        # product_object['description'] = response.css("div#info").get()
        
        #description in string format
        #get all strings in response tag
        description_list = response.css("div#info::text").getall()
        #join all the strings
        description = ' '.join(description_list)
        product_object['description'] = description

        yield product_object