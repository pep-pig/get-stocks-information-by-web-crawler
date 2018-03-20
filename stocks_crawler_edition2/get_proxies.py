import requests
from bs4 import  BeautifulSoup
class GetProxies(object):
    '''从https://free-proxy-list.net上抓取免费的代理存储到本地'''
    def __init__(self):
        '''类的数据为html响应'''
        self.response = self.get_html()
        self.proxies = []

    def get_html(self):
        '''利用request库获取html页面'''
        url = 'https://free-proxy-list.net'
        head ={'User-Agent': "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"}
        response = requests.get(url,headers = head )
        return  response.text

    def process_response(self):
        '''利用beautifulsoup库解析html页面'''
        soup = BeautifulSoup(self.response,'html.parser')
        # print(soup.prettify())
        return soup

    def extract_proxies(self,soup):
        '''获取页面中的代理ip'''
        tr = soup.find_all('tr')
        tr.pop(0)
        tr.pop(300)
        for tag in tr:
            td = tag.find_all('td')
            ip = td[0].text
            port = td[1].text
            if td[6].text == 'no':
                protocol = 'http'
            else:
                protocol = 'https'
            proxy = protocol+':'+'//'+ip+':'+port
            if protocol == 'https':
                #根据目标网站的接受的协议，选择自己需要的代理
                self.proxies.append(proxy)

    def save_proxies(self):
        '''将ip存入本地txt'''
        f = open('proxies.txt','w',encoding='utf-8')
        for proxy in self.proxies:
            f.write(proxy+'\n')

if __name__=='__main__':
    free_proxies = GetProxies()
    soup  = free_proxies.process_response()
    free_proxies.extract_proxies(soup)
    free_proxies.save_proxies()
