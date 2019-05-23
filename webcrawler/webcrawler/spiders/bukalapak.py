# -*- coding: utf-8 -*-
# TODO : 
# []Location
# []Category
# []Seller Activity
# [v]Urljoin list product
# [v]Urljoin next page
import scrapy, datetime

from webcrawler.items import ProductItem

class BukalapakSpider(scrapy.Spider):
    name = 'bukalapak'
    allowed_domains = ['www.bukalapak.com']
    start_urls = [
        "https://www.bukalapak.com/c/komputer?from=category_home&page=1&search%5Bkeywords%5D=",
        # "https://www.bukalapak.com/c/perlengkapan-kantor?from=category_home&page=1&search%5Bkeywords%5D="
        ]

    def parse(self, response):
        products = response.css('div.basic-products ul.products li.col-12--2 article.product-display div.product-description')
        for product_detail in products:
            product_link = response.urljoin(product_detail.css('a::attr(href)').get())
            yield scrapy.Request(url=product_link, callback=self.parse_product)

        next_page = response.css('a.next_page::attr(href)').get()
        if(next_page is not None):
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)
    
    def parse_product(self, response):
        product_object = ProductItem()
        product_object['online_marketplace'] = self.name
        product_object['time_taken'] = datetime.datetime.now()
        product_object['url'] = response.url
        
        #title and image url in string format
        product_object['title'] = response.css('h1.c-product-detail__name.qa-pd-name::text').get()
        product_object['image_url'] = response.css("div.c-product-image-gallery picture img::attr(src)").get()
        
        #get price data in string '1234567'
        price = response.css('div.c-product-detail-price::attr(data-reduced-price)').get()
        #convert into currency format 'Rp 1.234.567'
        # price_formatted = f'Rp{float(price):,.0f}'.replace(',','.')
        product_object['price_final'] = float(price)

        #stock data in string format '\n> 50 stok\n'
        #replace() for removing '\n'
        product_object['stock'] = response.css('div.qa-pd-stock strong span::text').get().replace('\n','')
        
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
        discount_formatted = float(discount.replace('%',''))
        product_object['discount'] = discount_formatted
        
        #rating data in float format
        rating = response.css('span.c-product-rating__value.is-hidden::text').get()
        product_object['rating'] = float(rating)

        #get condition data in string 'Baru' / 'Bekas'
        condition = response.css('dd.c-deflist__value.qa-pd-condition-value span.c-label::text').get()
        #check condition status
        #'Baru' = new_product
        if condition == 'Baru': new_product = 1 
        else: new_product = 0
        product_object['condition'] = new_product
        
        #seller and seller url in string format
        product_object['seller'] = response.css('a.c-user-identification__name.qa-seller-name::text').get()
        product_object['seller_url'] = response.urljoin(response.css('a.c-user-identification__name.qa-seller-name::attr(href)').get())
        
        #get seller location data in string format
        #convert into defined location data from location data in marketplace
        product_object['seller_location'] = response.css("span.c-user-identification-location__txt.qa-seller-location a::text").get()
        
        #convert into defined category data from start url 
        # product_object['category'] = str(response.css("dd.c-deflist__value.qa-pd-category-value.qa-pd-category::text").get()).replace("\n","")
        
        #description in string HTML format
        product_object['description'] = response.css("div.qa-pd-description p").get()

        yield product_object