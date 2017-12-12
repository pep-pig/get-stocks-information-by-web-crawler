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
		r = self.getHTMLText()
		soup = BeautifulSoup(r,'html.parser')
		ul = soup.find('div',attrs={'id':'quotesearch'}).find('ul')
		a=ul.find_all('a')
		for i in a:
			try:
				href=i.attrs['href']
				stock = re.findall(r"[s][hz]\d{6}", href)[0]
				url = "https://gupiao.baidu.com/stock/" + stock + ".html"
				yield scrapy.Request(url,callback = self.parse)
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
		infoDict = OrderedDict()
		soup = BeautifulSoup(response.body, 'html.parser')
		stockInfo = soup.find('div',attrs={'class':'stock-bets'})
		name = stockInfo.find_all(attrs={'class':'bets-name'})[0]
		infoDict.update({'股票名称': name.text.split()[0]})
		try:
			keyList = stockInfo.find_all('dt')
			valueList = stockInfo.find_all('dd')
			for i in range(len(keyList)):
				key = keyList[i].text
				val = valueList[i].text
				infoDict[key] = val
		except:
			pass
		yield infoDict
