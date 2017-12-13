# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo
from scrapy.conf import settings

class DropUncompleteItems(object):
    '''丢弃信息不全的股票'''
    def process_item(self,item,spider):
        try:
            item['今开']
            print('processing complete stock...')
            return item
        except:
            raise DropItem("droped uncomplete stocks:%s" %item['股票名称'])


class WritePipeline(object):
    '''将结果出入本地txt'''
    def open_spider(self, spider):
        self.f = open('StockInfo.txt', 'w')

    def close_spider(self, spider):
        self.f.close()

    def process_item(self, item, spider):
        try:
            #由于item内部本来就已经是utf-8的格式了，所以str一下以后，将会以utf-8的源码内容存储，
            #因此使用decode('string-escape')方法解码一次
            line = str(dict(item)).decode('string-escape') + '\n'
            print(line)
            self.f.write(line)
        except:
            pass
        return item

class SaveToMongodbPipeline(object):
    '''将结果写入MONGODB'''
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbName = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host = host,port = port)
        collection = client[dbName]
        self.stocks_info = collection[settings['MONGODB_COLLECTION_NAME']]

    def process_item(self,item,spider):
        try:
            self.stocks_info.insert(item)
        except:
            pass
        return item