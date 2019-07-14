import scrapy
from scrapy.crawler import CrawlerProcess
from webcrawler.spiders.bukalapak import BukalapakSpider
from webcrawler.spiders.tokopedia import TokopediaSpider

def prosesCrawl():
    process = CrawlerProcess({
        'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    })
    #process.crawl(BukalapakSpider)
    process.crawl(TokopediaSpider)
    process.start()