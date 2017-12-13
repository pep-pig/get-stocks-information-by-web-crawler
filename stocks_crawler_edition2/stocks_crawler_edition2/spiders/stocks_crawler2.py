# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup
from scrapy.shell import inspect_response
import re
from collections import OrderedDict

#from stocks.items import StocksItem
#from scrapy.loader import ItemLoader

class StockSpider(scrapy.Spider):
	name = 'stocks_crawler2'
	def __init__(self):
		self.headers = {
		'Accept': '*/*',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
		'Accept-Encoding': 'gzip, deflate, sdch',
		'Accept-Language': 'zh-CN,zh;q=0.8'
		}

	def start_requests(self):
		'''先用requests库抓取东方财富网获得每支股票的地址'''
		r = self.getHTMLText()
		soup = BeautifulSoup(r,'html.parser')
		ul = soup.find('div',attrs={'id':'quotesearch'}).find('ul')
		a=ul.find_all('a')
		j=0
		for i in a:
			try:
				href=i.attrs['href']
				stock = re.findall(r"[s][hz]\d{6}", href)[0]
				url = "https://gupiao.baidu.com/stock/" + stock + ".html"
				yield scrapy.Request(url,callback = self.parse)
				j=j+1
				if j>200:
					break
			except:
				continue

	def getHTMLText(self):

		try:
			url = 'http://quote.eastmoney.com/stocklist.html'
			html = requests.get(url)
			html.raise_for_status()
			html.encoding = html.apparent_encoding
			return html.text
		except:
			return ""

	def parse(self,response):
		'''处理response的回调函数，作用为提取response中的股票信息，需要注意的是，在这里可以灵活应用
		item，既可以在items.py中把item的内容写死，即每个item的内容都一样，也可以不在items.py中设置item，
		回调函数的yields的任意一个字典都会作为item传入在后续的pipelines.py中，这也即使每一个item项数不同
		也没关系，比如有的股票信息可能比较全，有20多项，有的却只有几项'''
		infoDict = OrderedDict()
		soup = BeautifulSoup(response.body, 'html.parser')
		stockInfo = soup.find('div',attrs={'class':'stock-bets'})
		name = stockInfo.find_all(attrs={'class':'bets-name'})[0]
		first_key = '股票名称'
		infoDict.update({first_key: name.text.split()[0].encode('utf-8')})
		try:
			keyList = stockInfo.find_all('dt')
			valueList = stockInfo.find_all('dd')
			for i in range(len(keyList)):
				key = keyList[i].text.encode('utf-8')
				val = valueList[i].text.encode('utf-8')
				infoDict[key] = val
		except:
			pass
		yield infoDict
