# -*- coding: utf-8 -*-
# TODO : 
# [v]Location
# []Category is Not Dynamic
# [v]Seller Activity
import scrapy, datetime, pymongo

from webcrawler.items import ProductItem

class BukalapakSpider(scrapy.Spider):
    name = 'bukalapak'
    
    def start_requests(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["comparison-shopping-engine"]
        kota_collection = db["kota"]
        kategori_collection = db["kategori"]

        #urls = [
            # "https://www.bukalapak.com/c/komputer/desktop?from=navbar_categories&source=navbar",
            # "https://www.bukalapak.com/c/komputer/laptop?from=navbar_categories&source=navbar",
            #"https://www.bukalapak.com/c/komputer/monitor?from=navbar_categories&source=navbar",
        #]
        for kategori in kategori_collection.find():
            for url_bukalapak in kategori["bukalapak"]:
                #print(url_bukalapak)
                if url_bukalapak:
                    yield scrapy.Request(url=url_bukalapak, callback=self.parse, meta={
                "kota_collection" : kota_collection,
                "idkategori":kategori["idkategori"]
                })

        # for url_item in urls:
        #     yield scrapy.Request(url=url_item, callback=self.parse, meta={
        #         "collection" : kota_collection
        #     })

    def parse(self, response):
        kota_collection = response.meta["kota_collection"]
        idkategori = response.meta["idkategori"]
        products = response.css('div.basic-products ul.products li.col-12--2 article.product-display div.product-description')
        #if products :
        #follow each product links
        for product_detail in products:
            product_link = response.urljoin(product_detail.css('a::attr(href)').get())
            yield scrapy.Request(url=product_link, callback=self.parse_product, meta={
                "kota_collection" : kota_collection,
                "idkategori" : idkategori
                })

        #go to the next page
        next_page = response.css('a.next_page::attr(href)').get()
        if(next_page is not None):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse, meta={
                "kota_collection" : kota_collection,
                "idkategori" : idkategori
            })
    
    def parse_product(self, response):
        kota_collection = response.meta["kota_collection"]

        #set condition status to 1, default is 1 "Baru"
        new_product = 1
        #get condition data in string 'Baru' / 'Bekas'
        condition = response.css('dd.c-deflist__value.qa-pd-condition-value span.c-label::text').get()
        #check condition status
        if condition == 'Bekas': new_product = 0
        if  new_product :
            product_object = ProductItem()
        
            product_object['condition'] = new_product
        
            product_object['online_marketplace'] = self.name
            product_object['time_taken'] = datetime.datetime.now()
            product_object['url'] = response.url
        
            #title and image url in string format
            product_object['title'] = response.css('h1.c-product-detail__name.qa-pd-name::text').get()
            product_object['image_url'] = response.css("div.c-product-image-gallery picture img::attr(src)").get()
        
            #get price data in string '1234567'
            price = response.css('div.c-product-detail-price::attr(data-reduced-price)').get()
            #convert into currency format 'Rp1.234.567'
            # price_formatted = f'Rp{float(price):,.0f}'.replace(',','.')
            #convert into float format
            product_object['price_final'] = float(price)

            #stock data in string format ex.'\n> 50 stok\n'
            #replace() for removing '\n'
            if response.css('div.qa-pd-stock strong span::text').get():
                product_object['stock'] = response.css('div.qa-pd-stock strong span::text').get().replace('\n','')
        
            #set original price with the same value as final price
            product_object['price_original'] = float(price)
            #set discount to 0.0
            product_object['discount'] = float(0)
            #check discount
            is_discount = response.css('div.c-product-detail-price span.c-product-detail-price__original span.amount::text').get() is not None
            if(is_discount):
                #get price data in string '1234567'
                price_original = response.css('div.c-product-detail-price span.c-product-detail-price__original span.amount::text').get().replace(".","")
                #convert into currency format 'Rp 1.234.567'
                # price_original_formatted = f'Rp{float(price_original):,.0f}'.replace(',','.')
                product_object['price_original'] = float(price_original)

                #get discount data in string '1%'
                discount = response.css('div.c-badge__content::text').get()
                #convert into float format  '1.0'
                discount = float(discount.replace('%',''))
                product_object['discount'] = discount
        
            #set rating to 0.0
            product_object['rating'] = float(0)
            #get rating data in string '5.0'
            rating = response.css('span.c-product-rating__value.is-hidden::text').get()
            if rating is not None:
                #convert into float format
                product_object['rating'] = float(rating)
            
            #seller and seller url in string format
            product_object['seller'] = response.css('a.c-user-identification__name.qa-seller-name::text').get()
            product_object['seller_url'] = response.urljoin(response.css('a.c-user-identification__name.qa-seller-name::attr(href)').get())
        
            #get seller location data in string format
            #convert into defined location data from location data in marketplace
            location_string = response.css("span.c-user-identification-location__txt.qa-seller-location a::text").get()
            location_string = str(location_string).upper().replace("KAB.", "KABUPATEN")   
            #get "kota" data from database
            #then assing seller_location with "idkota"
            kota = kota_collection.find_one({"namaKota" : {"$regex" : ".*{}.*".format(location_string)}})
            #idkota = ""
            #if kota is not None:
            #    idkota = kota["idKota"]
            product_object['seller_location'] = kota["namaKota"]
        
            #get seller last activity in string format
            product_object['last_activity'] = response.css('td.qa-seller-last-login-value time.last-login::text').get()

            #convert into defined category data from start url 
            # product_object['category'] = str(response.css("dd.c-deflist__value.qa-pd-category-value.qa-pd-category::text").get()).replace("\n","")
            #'Dsktp' : Desktop
            #'Lptop' : Laptop
            #'Mntr' : Monitor
            product_object['category'] = response.meta["idkategori"]
        
            #description in string HTML format
            # product_object['description'] = response.css("div.qa-pd-description p").get()
        
            #description in string format
            #get all strings in response tag
            description_list = response.css("div.qa-pd-description p::text").getall()
            #join all the strings
            description = ' '.join(description_list)
            product_object['description'] = description

            yield product_object