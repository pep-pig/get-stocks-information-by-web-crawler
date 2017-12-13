from pymongo import MongoClient
def test():
    '''pymongo与mongdb'''
    FENGJB = MongoClient()
    db1 = FENGJB.stocks
    collection11 = db1.stocks_info
    db2 = FENGJB.videos
    collection21 = db2.videos_info
    name1= {'股票名称':'中国中车'}
    name2= {'电影名称':'夏洛特烦恼'}
    collection11.insert(name1)
    collection21.insert(name2)

if __name__=='__main__':
    test()