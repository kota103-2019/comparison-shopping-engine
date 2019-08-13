# -*- coding: utf-8 -*-
import scrapy, datetime

from webcrawler.items import ProductItem

class ShopeeSpider(scrapy.Spider):
    name = 'shopee'

    def start_requests(self):
        urls = [
            'https://shopee.co.id/Komputer-Aksesoris-cat.134'
        ]
        for url_item in urls:
            yield scrapy.Request(url=url_item, callback=self.parse, meta={
                'splash':{
                    'args':{
                        'html':1,
                        'wait':5,
                        # 'proxy':'http://10.10.0.6:3128',
                    }
                },
                'pagenum': 1,
            })

    def parse(self, response):
        # print(response)
        page = response.meta['pagenum']
        products = response.css("div.shopee-search-item-result__item div")
        #follow each product links
        for product_detail in products:
            product_link = product_detail.css("a::attr(href)").get()
            product_link = response.urljoin(product_link)
            yield scrapy.Request(url=product_link, callback=self.parse_product, meta={
                'splash':{
                    'args':{
                        'html':1,
                        'wait':5,
                        # 'proxy':'http://10.10.0.6:3128',
                    }
                }
            })
        
        next_page = "https://shopee.co.id/Komputer-Aksesoris-cat.134?sortBy=pop&page=" + str(page)
        print(next_page)
        if(page < 50):
            yield scrapy.Request(url=next_page, callback=self.parse, meta={
                'splash':{
                    'args':{
                        'html':1,
                        'wait':5,
                        # 'proxy':'http://10.10.0.6:3128',
                    }
                },
                'pagenum': page+1,
            })
        # #go to the next page
        # next_page = response.css("a.GUHElpkt::attr(href)").get()
        # if(next_page is not None):
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(url=next_page, callback=self.parse, meta={
        #     })

    def parse_product(self, response):

        product_object = ProductItem()
        product_object['online_marketplace'] = self.name
        product_object['time_taken'] = datetime.datetime.now()
        product_object['url'] = response.url
        
        print(response.url)
        #title and image url in string format
        product_object['title'] = response.css("div._2TJgvU div.qaNIZv::text").get()
        # product_object['image_url'] = response.css("div._1eNVDM div._1anaJP div._3ZDC1p div::attr(style)").re(r'background-image: \s*(.*)')
        
        #get price data in string '1234567'
        price = response.css("div._3n5NQx::text").get()
        #cleaning up data, deleting 'Rp' and '.'
        price = price.replace('Rp','').replace('.','')
        #convert into float format
        product_object['price_final'] = float(price)
        
        # stock = response.css("div.kIo6pj").get()
        spek_list = response.css("div._2aZyWI div.kIo6pj")
        for spek in spek_list :
            if (spek.css("label::text").get() == "Stok"):
                stock = spek.css("div::text").get()
                stock = int(stock)
        

        
        # #stock data are not found
        # #replace with 'Informasi Stok Barang tidak Ditemukan'
        product_object['stock'] = stock
        
        #set original price with the same value as final price
        product_object['price_original'] = float(price)
        #set discount to 0.0
        product_object['discount'] = float(0)
        #check discount
        is_discount = response.css('div.MITExd::text').get() is not None
        if(is_discount):
            #get price data in string '1234567'
            price_original = response.css('div._3_ISdg::text').get()
            #cleaning up data, deleteting 'Rp' and '.'
            price_original = price_original.replace('Rp','').replace('.','')
            #convert into float format
            product_object['price_original'] = float(price_original)

            #get discount data in string '-1%'
            discount = response.css('div.MITExd::text').get()
            #cleaning up data, deleting '%' and '-'
            discount = discount.replace('% off','')
            #convert into float format '1.0'
            product_object['discount'] = float(discount)

        #set rating to 0.0
        product_object['rating'] = float(0)
        #get rating data in string '5.0'
        rating = response.css("div._2z6cUg._3Oj5_n::text").get()
        if rating is not None:
            #convert into float format
            product_object['rating'] = float(rating)
        
        #assumed product condition is new => 'Baru' = new_product
        new_product = 1
        product_object['condition'] = new_product
        
        #seller and seller url in string format    
        #get seller location data in string format
        #convert into defined location data from location data in marketplace
        #seller = response.css('div.seller-link a::attr(href)')
        product_object['seller'] = response.css('div._1Sw6Er div._2S9T8Y div._3Lybjn::text').get()
        # product_object['seller_url'] = response.css('div.seller-name__wrapper div.seller-name__detail a::attr(href)').get()
        #get seller location in string format

        # product_object['seller_location'] = 
        
        spekk_list = response.css("div._2aZyWI div.kIo6pj")
        for spekk in spekk_list :
            if (spekk.css("label::text").get() == "Dikirim Dari"):
                seller_location = spekk.css("div::text").get()


                product_object['seller_location'] = seller_location

        #get seller last activity in string format
        last_activity = response.css('div._2S9T8Y div._1h7HJr::text').get()
        last_activity = last_activity.replace('Aktif ', '')
        product_object['last_activity'] = last_activity
        
        # #convert into defined category data from start url 
        # product_object['category'] = idkategori
        
        #description in string HTML format
        description_list = response.css('div._2C2YFD div._2aZyWI div._2u0jt9 span::text').get()
        #join all the strings
        # description = ' '.join(description_list)
        product_object['description'] = description_list

        yield product_object
        # print(description_list)