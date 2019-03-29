# -*- coding: utf-8 -*-
import scrapy


class BukalapakSpider(scrapy.Spider):
    name = 'bukalapak'
    # allowed_domains = ['https://www.bukalapak.com/c/komputer/laptop']
    start_urls = ['https://www.bukalapak.com/c/komputer/laptop?page=1']

    def parse(self, response):
        # for li in response.css('li.col-12--2'):
        # print(li.css('a::attr(href)').get())

        print('current page : ' + response.url)
        next_page_object = response.css('a.next_page::attr(href)').get()
        if(next_page_object is not None):
            next_page = str(next_page_object)
            page_num = next_page.split('?page=')
            next_page = 'https://www.bukalapak.com' + next_page
            if int(page_num[1]) < 10:
                print('next page : ' + next_page)
                yield response.follow(next_page, callback=self.parse)
