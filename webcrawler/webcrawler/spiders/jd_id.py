# -*- coding: utf-8 -*-
import scrapy, datetime

from webcrawler.items import ProductItem

class JdIdSpider(scrapy.Spider):
    name = 'jd.id'
    allowed_domains = ['www.jd.id']
    start_urls = [
        'https://www.jd.id/category/jual-pc-875061492.html'
        ]

    def parse(self, response):
        products = response.css('div.item div.p-desc')
        for product_detail in products:
            product_link = response.urljoin(product_detail.css('a::attr(href)').get())
            yield scrapy.Request(url=product_link, callback=self.parse, meta={
                'splash':{
                    'args':{
                        'html':1,
                        # 'proxy':'http://10.10.0.6:3128',
                    },

                    'endpoint':'render.html',
                }
            })
        
        next_page_object = response.urljoin(response.css('div.pagination a.p-next::attr(href)').get())
        if(next_page_object is not None):
            next_page = str(next_page_object)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_product(self, response):
        product_object = ProductItem()
        product_object['online_marketplace'] = self.name
        product_object['time_taken'] = datetime.datetime.now()
        product_object['url'] = response.url
        is_jdid_product = response.css("div#summary h1.tit span::text").get() == 'JD.id'
        if(is_jdid_product):
            product_object['title'] = response.css("div#summary h1.tit span::text")[1].get()
        else:
            product_object['title'] = response.css("div#summary h1.tit span::text").get()
        product_object['image_url'] = response.urljoin(response.css("div.big-img-cntnr img::attr(src").get())
        product_object['price_final'] = response.css("div.price div.dd span.sale-price::text").get()
        product_object['price_original'] = response.css("div.lastprice div.dd::text").get()
        product_object['rating'] = response.css("div.scores span.number::text").get()
        product_object['condition'] = "Baru"
        if(is_jdid_product):
            product_object['seller'] = "JD.id"
            product_object['seller_url'] = "JD.id"
            product_object['seller_location'] = "JD.id"
        else:
            pass
        # product_object['category'] = response
        # product_object['description'] = response