# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

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
            line = str(item).decode('string-escape') + '\n'
            print(line)
            self.f.write(line)
        except:
            pass
        return item