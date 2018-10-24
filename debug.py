from scrapy import cmdline
#cmdline.execute("cd H:\OneDrive\Mysql\get-stock-information-to-Mysql".split(' '))
cmdline.execute("scrapy crawl stocks_info_spider".split())
