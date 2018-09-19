# 两个功能不同的爬虫

from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)              # 连接MongoDB
second_hand = client['second_hand']                           # 新建一个数据库
url_list = second_hand['url_list']                            # 在数据库中新建一个用于存储要爬取的url的表
information_list = second_hand['information_list']            # 新建一个用于存储爬取的商品信息的表



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3387.400 QQBrowser/9.6.11984.400',
    'Cookie':'__admx_track_id=Y60CHGi9KHQtLT6q7B_QYQ; __admx_track_id.sig=svjv-80R4st1VtNoJ83Ul6iA_uQ; __trackId=151193014726415; __city=guangzhou; appVersion=5.7.1; __smartphone=1536477219; Hm_lvt_767685c7b1f25e1d49aa5a5f9555dc7d=1536477221; __s=l3bjicv3koph502ed4hu40clf3; _ga=GA1.2.1719751513.1536477060; _gid=GA1.2.1476441797.1536477060; Hm_lvt_5a727f1b4acc5725516637e03b07d3d2=1536476509,1536539297,1536644290,1536644872; Hm_lpvt_5a727f1b4acc5725516637e03b07d3d2=1536659589; __sense_session_pv=5',
}


# spider1获取所有商品的链接
# http://guangzhou.baixing.com/shouji/posterType_%E4%B8%AA%E4%BA%BA/?page=2
# http://guangzhou.baixing.com/diannao/posterType_%E4%B8%AA%E4%BA%BA/?page=2
def goods_links_page(link_class, page):
    url = '{}posterType_%E4%B8%AA%E4%BA%BA/?page={}'.format(link_class, page)
    html = requests.get(url, headers=headers).text
    time.sleep(1)
    soup = BeautifulSoup(html, 'lxml')
    if soup.select('li span'):                            # 判断 如果在有效的页数内 则进行抓取
        for goods_link in soup.select('.media-body-title a[href]'):  # 遍历含有要抓取的url的标签
            link = goods_link.get('href')
            # second_hand.url_list.drop()                 # 清除数据库中的表
            # url_list.insert_one({'url': link})          # 写入数据库
            print(link)
    else:                                                 # 不在有效页数 则跳过
        pass


# spider2 获取商品的信息
def goods_information(url):
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    if soup.select('.viewad-content.out-of-time'):                    # 判断 商品是否过期或者被买
        pass
    else:                                                             # 是正常的商品 则进行抓取
        title = soup.select('.viewad-title')[0].get_text().replace('\xa0', '')
        price = soup.select('.viewad-actions .price')[0].get_text().replace('\t', '')
        date = soup.select('.viewad-actions [data-toggle="tooltip"]')[0].get_text().replace('\xa0', '')
        area = soup.select('.meta-address')[0].get_text()
        url = url
        # second_hand.information_list.drop()                                                         # 清除数据库中的表
        #information_list.insert_one({'title': title, 'price': price, 'date': date, 'area': area, 'url': url})   # 写入数据库
        # print(information_list.count())
        # print(title)


# 调试用代码：

# # goods_links_page('http://guangzhou.baixing.com/shouji/', 100)
# for item in url_list.find():
#     print(item)
# print(url_list.find().count())


n = 0
# goods_information('http://guangzhou.baixing.com/shouji/a1480292035.html?from=regular')
# for item in information_list.find():
#     print(item)
#     n += 1
# print(n)
# print(information_list.count())


