# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exporters import JsonItemExporter, JsonLinesItemExporter
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

class JsonPipeline(object):
    def __init__(self):
        self.file = open("result.json", 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

# class JsonLineItemPipeline(object):
#     def open_spider(self, spider):
#         self.product = {}

#     def close_spider(self, spider):    

#     def process_item(self, spider):

class MongoDBPipeline(object):
    

    def __init__(self):
        client = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
            )
        # client = pymongo.MongoClient('mongodb+srv://KoTA-103:bismillah@cluster0-sr9cz.mongodb.net/test?retryWrites=true&w=majority')
        db = client[settings['MONGODB_DATABASE']]
        self.collection = db[settings['MONGODB_COLLECTION']]
    
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database!", level=log.DEBUG, spider=spider)

        return item
