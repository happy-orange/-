# 问题：请求过于频繁ip被封
# 解析view(浏览量)时速度太慢了

from bs4 import BeautifulSoup
import requests
import urllib.parse
import json
import random
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3387.400 QQBrowser/9.6.11984.400',
    'Cookie': '__admx_track_id=Y60CHGi9KHQtLT6q7B_QYQ; __admx_track_id.sig=svjv-80R4st1VtNoJ83Ul6iA_uQ; __trackId=151193014726415; __city=guangzhou; appVersion=5.7.1; __smartphone=1536477219; Hm_lvt_767685c7b1f25e1d49aa5a5f9555dc7d=1536477221; __s=fakrc7iacd5346vtafe31qqsg3; _auth_redirect=http%3A%2F%2Fguangzhou.baixing.com%2Fpingbandiannao%2F; _ga=GA1.2.1719751513.1536477060; _gid=GA1.2.1476441797.1536477060; _gat=1; __sense_session_pv=4; Hm_lvt_5a727f1b4acc5725516637e03b07d3d2=1536476509,1536539297; Hm_lpvt_5a727f1b4acc5725516637e03b07d3d2=1536545558',
}
# 设置代理
proxy_list = [
    'http://183.62.22.220:3218',
    'http://182.246.221.130:80',
    'http://180.109.168.67:8118',
    ]
proxy_ip = random.choice(proxy_list)
proxies = {'http': proxy_ip}


def get_links_total(selsects, page):           # 解析本页中的所有link
    links = []
    url = 'http://guangzhou.baixing.com/pingbandiannao/posterType_{}/?page={}'.format(selsects, page)
    print(url)
    html = requests.get(url, headers=headers,).text
    time.sleep(random.randint(0, 2))                   # 随机延时0到2s
    soup = BeautifulSoup(html, 'lxml')

    for link in soup.select('.media-body-title a[href]'):
        links.append(link.get('href'))
        #break
    # print(len(links))
    return links


def get_views_total(links):                  # 解析links中的所有view
    views = []
    for link in links:
        id = str(link).split('/a')[1].split('.')[0]
        view = 'http://guangzhou.baixing.com/arch/ad_counter?id={}'.format(str(id))
        html = requests.get(view, headers=headers,).text
        time.sleep(random.randint(0, 2))      # 随机延时0到2s
        soup = BeautifulSoup(html, 'lxml')
        view_json = soup.text
        view = json.loads(view_json)['count']
        views.append(view)
        # break
    print(len(views))
    return views


def get_msg(selsects='个人', pages=1):
    selsects = url_turn(selsects)               # 因为url中含有中文，所以要用此方法将中文转化为对应的编码(我也不知道是什么编码)
    for page in range(pages+1)[1:]:             # 先遍历要爬取的总页数
        links = get_links_total(selsects, page)
        views = get_views_total(links)
        for link, view in zip(links, views):       # 逐页逐页地爬取，并把之前获取的links和views遍历到字典里面
            html = requests.get(link, headers=headers,).text
            time.sleep(random.randint(0, 2))       # 随机延时0到2s
            soup = BeautifulSoup(html, 'lxml')
            title = soup.select('.viewad-title')
            price = soup.select('.viewad-actions .price')
            date = soup.select('.viewad-actions [data-toggle="tooltip"]')
            area = soup.select('.meta-address')
            classify = soup.select('.meta-posterType')
            view = view
            data = {
                'title': str(title[0].get_text()).replace('\xa0', ''),   # 清洗一下数据
                'price': str(price[0].get_text()).replace('\t', ''),
                'date': str(date[0].get_text()).replace('\xa0', ''),
                'area': str(area[0].get_text()).replace('\xa0', ''),
                'classify': classify[0].get_text(),
                'view': view,
            }
            if '搞定了！'in data['title']:                # 如果商品被卖了，就跳过，不抓取
                continue
            print(data)


def url_turn(chinese):              # 将中文转化为对应的编码
    return urllib.parse.quote(chinese)


get_msg('个人', 4)

# get_links_total('%E4%B8%AA%E4%BA%BA', 1)
# get_views_total()


# # 用于测试ip是否被封
#
# link = 'http://guangzhou.baixing.com/pingbandiannao/posterType_个人?'
# html = requests.get(link, headers=headers,).content
# soup = BeautifulSoup(html, 'lxml')
# print(soup)

