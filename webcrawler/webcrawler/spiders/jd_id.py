# -*- coding: utf-8 -*-
#[v]Location
#[]Category is Not Dynamic
import scrapy, datetime , pymongo

from webcrawler.items import ProductItem

class JdIdSpider(scrapy.Spider):
    name = 'jd.id'

    def start_requests(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["comparison-shopping-engine"]
        kategori_collection = db["kategori"]
        # kota_collection = db["kota"]

        # urls = [
        #     "https://www.jd.id/category/jual-monitor-875061553.html",
        # ]
        for kategori in kategori_collection.find():
            for url_item in kategori["jdId"]:
                if url_item :
                    #print("KATEGORI ID"+ kategori["idkategori"])
                    idkat = kategori["idkategori"]
                    yield scrapy.Request(url=url_item, callback=self.parse, meta={
                        "kategori" : kategori["idkategori"]
                    })
                    # yield scrapy.Request(url=url_item, callback=self.parse, meta={"kategori":kategori["idkategori"]})
        # for kategori in kategori_collection.find():
        #     for url_jdId in kategori["jdId"]:
        #         #print(url_bukalapak)
        #         if url_jdId:
        #             print(kategori["idkategori"])
        #             yield scrapy.Request(url=url_jdId, callback=self.parse, meta={"kategori":kategori["idkategori"]},)

    def parse(self, response):
        products = response.css('div.item div.p-desc')
        #print(response.meta["kategori"])
        # idkat = ""
        idkat = response.meta["kategori"]
        #print(idkat)
        #follow each product links
        for product_detail in products:
            product_link = response.urljoin(product_detail.css('a::attr(href)').get())
            yield scrapy.Request(url=product_link, callback=self.parse_product, meta={
                'splash':{
                    'args':{
                        'html':1,
                        # 'proxy':'http://10.10.0.6:3128',
                    },
                },
                "idkategori": idkat
            })
        
        #go to the next page
        next_page_object = response.urljoin(response.css('div.pagination a.p-next::attr(href)').get())
        if(next_page_object is not None):
            next_page = str(next_page_object)
            yield scrapy.Request(url=next_page, callback=self.parse, meta={
                        "kategori" : response.meta["kategori"]
                    })


    def parse_product(self, response):
        idkategori = response.meta["idkategori"]

        product_object = ProductItem()
        product_object['online_marketplace'] = self.name
        product_object['time_taken'] = datetime.datetime.now()
        product_object['url'] = response.url
        
        #check jd.id product
        #title data in string format 
        is_jdid_product = response.css("div#summary h1.tit span::text").get() == 'JD.id'
        if(is_jdid_product):
            product_object['title'] = response.css("div#summary h1.tit span::text").getall()[1]
        else:
            product_object['title'] = response.css("div#summary h1.tit span::text").get()
        #image_url in string format
        product_object['image_url'] = response.urljoin(response.css("div.big-img-cntnr img::attr(src)").get())
        
        #get price data in string'123,456,789'
        price = response.css("div.price div.dd span.sale-price::text").get()
        #convert into float format
        product_object['price_final'] = float(price.replace(',',''))

        #stock data in string format ex.'Stok sedikit'
        product_object['stock'] = response.css('div.dd div#store-prompt::text').get()
        
        #set original price with the same value as final price
        product_object['price_original'] = float(price.replace(',',''))
        #set discount to 0.0
        product_object['discount'] = float(0)
        #check discount
        is_discount = response.css("div.lastprice div.dd::text").get()
        if(is_discount):
            #get price data in string 'Rp 1,234,567'
            price_original = response.css("div.lastprice div.dd::text").get()
            #cleaning up data, deleting "Rp " and ","
            price_original = price_original.replace('Rp ','').replace(',','')
            #convert into float format
            product_object['price_original'] = float(price_original)

            #get discount data in string '5% OFF'
            discount = response.css('div.item div.dd span.discount-rate::text').get()
            #cleaning up data, deleting '% OFF'
            discount = discount.replace('% OFF','')
            #convert into float format '5.0'
            product_object['discount'] = float(discount)
        
        #set rating to 0.0
        product_object['rating'] = float(0)
        #get rating data in string'5.0'
        rating = response.css("div.scores span.number::text").get()
        if rating is not None:
            #convert into float format
            product_object['rating'] = rating

        #assumed product condition is new => 'Baru' = new_product
        new_product = 1
        product_object['condition'] = new_product
        
        if(is_jdid_product):
            #if the seller is JD.id
            product_object['seller'] = "JD.id"
            product_object['seller_url'] = "https://jd.id"
            product_object['seller_location'] = "Informasi Lokasi Penjual tidak Ditemukan"
        else:
            #seller in string format
            product_object['seller'] = response.css('div.seller-name div.title-right h2.name::text').get()
            #seller_url in string format
            product_object['seller_url'] = response.urljoin(response.css('div.seller-name div.title-right a.clickable::attr(href)').get())
            product_object['seller_location'] = "Informasi Lokasi Penjual tidak Ditemukan"

        #get seller last activity in string format
        product_object['last_activity'] = "Informasi tidak Ditemukan"

        #convert into defined category data from start url     
        #'Dsktp' = Desktop
        #'Lptop' : Laptop
        #'Mntr' : Monitor
        product_object['category'] = idkategori

        #description in string HTML format
        # product_object['description'] = response

        #description in string format
        #get all strings in response tag
        description_list = response.css('div.p-about div.description.item div.cnt p span::text').getall()
        #join all the strings
        description = ' '.join(description_list)
        product_object['description'] = description

        yield product_object