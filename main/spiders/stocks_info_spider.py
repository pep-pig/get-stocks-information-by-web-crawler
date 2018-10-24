# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from collections import OrderedDict
import time
import re
from datetime import datetime
class StockSpider(scrapy.Spider):
	name = 'stocks_info_spider'
	def __init__(self):
		self.headers = {
		'Accept': '*/*',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'zh-CN,zh;q=0.8'
		}

	def start_requests(self):
		'''
		抓取20个公司的股票信息：

		银行类：
		浦发银行：https://gupiao.baidu.com/stock/sh600000.html
		招商银行：https://gupiao.baidu.com/stock/sh600036.html
		工商银行：https://gupiao.baidu.com/stock/sh601398.html
		建设银行：https://gupiao.baidu.com/stock/sh601939.html
		中国银行：https://gupiao.baidu.com/stock/sh601988.html

		证券类：
		中信证券：https://gupiao.baidu.com/stock/sh600030.html
		光大证券：https://gupiao.baidu.com/stock/sh601788.html
		广发证券：https://gupiao.baidu.com/stock/sz000776.html
		招商证券：https://gupiao.baidu.com/stock/sh600999.html
		长江证券：https://gupiao.baidu.com/stock/sz000783.html

		科技类：
		上汽集团：https://gupiao.baidu.com/stock/sh600104.html
		美的集团：https://gupiao.baidu.com/stock/sz000333.html
		东软集团：https://gupiao.baidu.com/stock/sh600718.html
		联想集团：https://gupiao.baidu.com/stock/hk00992.html
		上港集团：https://gupiao.baidu.com/stock/sh600018.html

		地产类：
		万科地产：https://gupiao.baidu.com/stock/hk02202.html
		恒大地产：https://gupiao.baidu.com/stock/hk03333.html
		绿地地产：https://gupiao.baidu.com/stock/sh600606.html
		保利地产：https://gupiao.baidu.com/stock/sh600048.html
		碧桂园地产：https://gupiao.baidu.com/stock/hk02007.html
		:return:
		'''
		targetUrl = [
		'https://gupiao.baidu.com/stock/sh600000.html',
		'https://gupiao.baidu.com/stock/sh600036.html',
		'https://gupiao.baidu.com/stock/sh601398.html',
		'https://gupiao.baidu.com/stock/sh601939.html',
		'https://gupiao.baidu.com/stock/sh601988.html',
		]

		while True:
			if (datetime.now().strftime('%H:%M:%S')>'09:30:00' and datetime.now().strftime('%H:%M:%S')<'11:30:00') or (datetime.now().strftime('%H:%M:%S')>'13:00:00' and datetime.now().strftime('%H:%M:%S')<'15:00:00'):
				time.sleep(5)
				for url in targetUrl:
					yield scrapy.Request(url,callback = self.parse,dont_filter=True)

	def parse(self,response):
		'''处理response的回调函数，作用为提取response中的股票信息，需要注意的是，在这里可以灵活应用
		item，既可以在items.py中把item的内容写死，即每个item的内容都一样，也可以不在items.py中设置item，
		回调函数的yields的任意一个字典都会作为item传入在后续的pipelines.py中，这也即使每一个item项数不同
		也没关系，比如有的股票信息可能比较全，有20多项，有的却只有几项'''
		infoDict = {}
		soup = BeautifulSoup(response.body, 'html.parser')
		stockInfo = soup.find('div',attrs={'class':'stock-bets'})
		if stockInfo!=None:
			name = stockInfo.find_all(attrs={'class':'bets-name'})[0]
			infoDict['股票名称']=name.text.strip('\n').split()[0]
			infoDict['实时价格']=float(stockInfo.find_all(attrs={'class':'_close'})[0].text.strip('\n').split()[0])
			infoDict['涨跌幅度']=float(''.join(list(stockInfo.find_all('span')[3].text.strip('\n').split()[0])[0:4]))

			keyList = stockInfo.find_all('dt')
			valueList = stockInfo.find_all('dd')
			for i in range(len(keyList)):
				key = keyList[i].text.strip('\n')
				try:
					val=float(re.match(r'^\-?[0-9]+\.?[0-9]+',valueList[i].text.strip()).group())
				except:
					val='NULL'
				infoDict[key] = val
			yield infoDict
