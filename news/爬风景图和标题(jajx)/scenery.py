'''
    今日头条搜索：风景，将爬取标题作为文件夹名字，将相应的图片下载进去
'''

import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool


# def url_turn(chinese):              # 将中文转化为对应的编码
#     return urllib.parse.quote(chinese)
# 获得要爬取的url
def get_page(offset):
    params = {
        'offset': offset,                # 通过offset来翻页
        'format': 'json',
        'keyword': '旅游',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
        'from': 'search_tab',
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url)                        # 或者用 requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()                          # 一般处理抓包响应时都用json()转化为dict
    except requests.ConnectionError:
        return None


# 爬取一个url的题目和图片的url
def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            if item.get('title'):
                title = str(item.get('title')).replace('/', ',')
                if item.get('image_list'):
                    images = item.get('image_list')
                    for image in images:
                        yield {
                            'image': image.get('url'),
                            'title': title,
                        }


# 下载图片
def save_image(item):                                          # 这里的item为get_page()中的image
    if not os.path.exists(item.get('title')):                  # os模块 用于文件操作 这里判断是否存在名为title的文件夹
        os.mkdir(item.get('title'))                            # os.mkdir 生成单级目录     os.mkdirs 生成多级目录
    try:
        response = requests.get('http:' + item.get('image'))           # 这里要把'http:'加上，不然无法下载
        if response.status_code == 200:                                # 问题：为什么把存储的路径换到py文件的下一级目录就报错？
            file_path = 'D:/爬虫项目/新闻系列/今日头条/爬风景图和标题(jajx)/{0}/{1}.{2}'.format(item.get('title'), md5(response.content).hexdigest(), '.jpg')
            if not os.path.exists(file_path):
                print('ok')
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')


def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        # print(item)
        save_image(item)


START = 1
END = 2

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(START-1, END)])             # 为什么要这样写?
    pool.map(main, groups)
    pool.close()
    pool.join()


# 测试：
# json = get_page(0)
# lists = get_images(json)
# image = list(lists)
# print(image[0])
# save_image(image[0])

