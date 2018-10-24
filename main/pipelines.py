# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymysql.cursors
from datetime import datetime
from scrapy.conf import settings

class DropUncompleteItems(object):
    '''丢弃信息不全的股票'''
    def __init__(self):
        self.diction={
            '浦发银行':0,
            '招商银行':0,
            '工商银行':0,
            '建设银行':0,
            '中国银行':0}
    def process_item(self,item,spider):
        if self.diction[item['股票名称']]==item['实时价格']:
            raise DropItem("%s的股价没有改变" % item['股票名称'])
        else:
            self.diction[item['股票名称']]=item['实时价格']
            return item
class MySQLPipeline(object):
    #从setttings文件获取类属性，所谓依赖注入

    @classmethod
    def from_crawler(cls, crawler):
        cls.DBNAME = crawler.settings.get('MYSQL_DBNAME')
        cls.HOST = crawler.settings.get('MYSQL_HOST')
        cls.PORT= crawler.settings.get('MYSQL_PORT')
        cls.USER= crawler.settings.get('MYSQL_USER')
        cls.PASSWD= crawler.settings.get('MYSQL_PASSWD')
        return cls()

    def open_spider(self,spider):
        self.connect = pymysql.Connect(
            host=self.HOST,
            port=self.PORT,
            user=self.USER,
            passwd=self.PASSWD,
            db=self.DBNAME,)
        # 获取游标
        self.cursor = self.connect.cursor()
        print('连接数据库成功')

    def close_spider(self,spider):
        self.cursor.close()
        self.connect.close()
        print('断开数据库连接成功')

    def process_item(self,item,spider):
        item['时间'] =datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = "INSERT INTO %s(时间,\
               实时价格,  今开,  成交量,  最高,  涨停,  内盘,  成交额, 委比, 流通市值, 市盈率MRQ, 每股收益, 总股本,\
               涨跌幅度,   昨收,  换手率,  最低,  跌停,  外盘,  振幅,   量比, 总市值,   市净率, 每股净资产, 流通股本 \
              )values('%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = (item['股票名称'],item['时间'],item['实时价格'],item['今开'],item['成交量'],item['最高'],item['涨停'],item['内盘'],
                item['成交额'],item['委比'],item['流通市值'],item['市盈率MRQ'],item['每股收益'],item['总股本'],
                item['涨跌幅度'],item['昨收'],item['换手率'],item['最低'],item['跌停'],item['外盘'],
                item['振幅'],item['量比'],item['总市值'],item['市净率'],item['每股净资产'],item['流通股本'])
        a= sql % data
        self.cursor.execute(sql % data)
        self.connect.commit()
        print('成功插入:',item['股票名称'])


