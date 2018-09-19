# 用于抓取所有分类的url

from bs4 import BeautifulSoup
import requests


url = 'http://guangzhou.baixing.com/ershou/?src=topbar'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3387.400 QQBrowser/9.6.11984.400',
    'Cookie': '__admx_track_id=Y60CHGi9KHQtLT6q7B_QYQ; __admx_track_id.sig=svjv-80R4st1VtNoJ83Ul6iA_uQ; __trackId=151193014726415; __city=guangzhou; appVersion=5.7.1; __smartphone=1536477219; Hm_lvt_767685c7b1f25e1d49aa5a5f9555dc7d=1536477221; __s=l3bjicv3koph502ed4hu40clf3; _ga=GA1.2.1719751513.1536477060; _gid=GA1.2.1476441797.1536477060; __sense_session_pv=10; Hm_lvt_5a727f1b4acc5725516637e03b07d3d2=1536476509,1536539297,1536644290,1536644872; Hm_lpvt_5a727f1b4acc5725516637e03b07d3d2=1536645160',
}
html = requests.get(url, headers=headers).text
soup = BeautifulSoup(html, 'lxml')
titles_class = soup.select('fieldset li')[1:24]
links_class = soup.select('fieldset li a')[1:24]


def get_links_class_total():
    for title_class, link_class in zip(titles_class, links_class):
        data = {
            'title': title_class.get_text(),
            'link': 'http://guangzhou.baixing.com'+link_class.get('href')
        }
        print(data['link'])


links_class_total = '''
    http://guangzhou.baixing.com/shouji/
    http://guangzhou.baixing.com/diannao/
    http://guangzhou.baixing.com/bijiben/
    http://guangzhou.baixing.com/pingbandiannao/
    http://guangzhou.baixing.com/shumachanpin/
    http://guangzhou.baixing.com/yinger/
    http://guangzhou.baixing.com/dianqi/
    http://guangzhou.baixing.com/jiaju/
    http://guangzhou.baixing.com/fushi/
    http://guangzhou.baixing.com/menpiao/
    http://guangzhou.baixing.com/zhaoxiangji/
    http://guangzhou.baixing.com/shoujipeijian/
    http://guangzhou.baixing.com/riyongpin/
    http://guangzhou.baixing.com/yundongqicai/
    http://guangzhou.baixing.com/nongchanpin/
    http://guangzhou.baixing.com/yueqi/
    http://guangzhou.baixing.com/bangongyongpin/
    http://guangzhou.baixing.com/bangongjiaju/
    http://guangzhou.baixing.com/qishipenjing/
    http://guangzhou.baixing.com/xuniwupin/
    http://guangzhou.baixing.com/qitazhuanrang/
'''