# -*- coding: utf-8 -*-
#[]Location
#[]Seller Information
#   has separate scraper
#[v]Seller Name
#[v]Seller Location
#[]Seller Last Activity
import time
import scrapy, datetime, pymongo

from webcrawler.items import ProductItem

class LazadaSpider(scrapy.Spider):
    name = 'lazada'
    def start_requests(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["comparison-shopping-engine"]
        kategori_collection = db["kategori"]

        for kategori in kategori_collection.find({}):
            for url_lazada in kategori["lazada"]:
                if url_lazada:
                    # print(url_lazada+" awal")
                    pageNum = 1
                    end = False
                    while pageNum<50 :
                        print("masuk while")
                        url = url_lazada +"?page="+str(pageNum)
                    
                        print(url+"masuk if")
                        time.sleep(3)
                        yield scrapy.Request(url=url, callback=self.parse, meta={
                            'splash':{
                                'args':{
                                    'html':1,
                                    'wait':1,
                                    # 'timeout':2400,
                                    # 'proxy':'http://10.10.0.6:3128',
                                },
                            },
                        "idkategori":kategori["idkategori"],
                        #"collection" : kota_collection,
                        })
                        pageNum +=1
                    
    def parse(self, response):
        products = response.css("div.c1_t2i div.c2prKC div.c3KeDq div.c16H9d")
        idkategori = response.meta["idkategori"]
        
        for product_detail in products:
            time.sleep(3)
            product_link = response.urljoin(product_detail.css("a::attr(href)").get())
            yield scrapy.Request(url=product_link, callback=self.parse_product, meta={
                'splash':{
                    'args':{
                        'html':1,
                        'wait':1,
                        # 'timeout':2400,
                        # 'proxy':'http://10.10.0.6:3128',
                    },
                },
                "idkategori" : idkategori
                } )

    def parse_product(self, response):
        idkategori = response.meta["idkategori"]
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
        
        #set original price with the same value as final price
        product_object['price_original'] = float(price)
        #set discount to 0.0
        product_object['discount'] = float(0)
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

        #set rating to 0.0
        product_object['rating'] = float(0)
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
        #seller = response.css('div.seller-link a::attr(href)')
        product_object['seller'] = response.css('div.seller-name__wrapper div.seller-name__detail a::text').get()

        product_object['seller_url'] = response.css('div.seller-name__wrapper div.seller-name__detail a::attr(href)').get()
        #get seller location in string format
        product_object['seller_location'] = "Informasi tidak Ditemukan"
        #get seller last activity in string format
        product_object['last_activity'] = "Informasi tidak Ditemukan"
        
        #convert into defined category data from start url 
        product_object['category'] = idkategori
        
        #description in string HTML format
        description_list = response.css('div.html-content span::text').getall()
        #join all the strings
        description = ' '.join(description_list)
        product_object['description'] = description
        
        yield product_object
