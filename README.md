# scrapy_stocks
scrapy+mongodb+proxy+user_agent to crawl stocks from https://gupiao.baidu.com/stock
具体细节可以查看官方的帮助文档，中文本版：https://scrapy-chs.readthedocs.io/zh_CN/latest/intro/tutorial.html#intro-tutorial
## technical route
* request and re :use 'requests' and 're' modules to extract each stocks code  from
* scrapy : use scrapy to get stocks information in detail from 
* beautiful soup : use beautiful soup to extract interested information from the html file.
* MongoDB : use mongodb to store data
## issues and solutions
* request header : many website will reject your request if you use the default request header<br>
`--solutions`: use header pool randomly in each request<br>
* agency : scrapy is a distributed crawler frame , so if you always use the same ip address ,there is a great chance that your ip will be banned.<br>
`--solutions`: To avoid banned , we can get many agencies from  ,and put the usable ips to our ip pool ,if our request rejected ,we can change a new ip .
## data postprocess
* pipeline technique: after getting data, then we can use pipelines to filter the data 
## configuration
* scrapy frame offer many configurations for user to set ,you can use appropriate setting for your own project .
