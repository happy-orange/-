# 爬取今日头条首页的焦点栏目的信息系
import requests
import json
import time

url = 'https://www.toutiao.com/api/pc/focus/'        # 通过查看Network中的XHR信息得出焦点栏目是该url通过JS加载的
html_json = requests.get(url).text
json_msg = json.loads(html_json)                     # 通过JS加载的都是json数据，要用此方法将json数据转化为字典
json_select = json_msg['data']['pc_feed_focus']      # 将需要的数据从字典中筛选出来
for i in json_select:
    title = i['title']
    url = 'https://www.toutiao.com' + i['display_url']
    img = 'http:' + i['image_url']
    print('title:' + title, 'url:' + url, 'img:' + img )









