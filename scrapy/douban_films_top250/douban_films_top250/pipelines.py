# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
import scrapy
from douban_films_top250.settings import IMAGES_STORE as img_store
from scrapy.pipelines.images import ImagesPipeline


class DoubanFilmsTop250Pipeline(object):
    def __init__(self):
        self.f = open('films_top250.json', 'wb')

    # 接收从spider返回来的item，写入json文件
    def process_item(self, item, spider):
        # 将字典转化为字符串
        content = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.f.write(content.encode('utf-8'))
        # 如果下面没有管道了则返回给引擎，如果还有别的管道文件则进入别的管道（在setting可设置管道的优先级）
        return item

    # 爬虫退出的时候执行，关闭打开的文件
    def close_spider(self, spider):
        self.f.close()


class DownLoadImgPipeline(ImagesPipeline):      # ImagesPipeline专门用于下载图片
    def get_media_requests(self, item, info):   # 改写scrapy\pipelines中的方法
        img_link = item['imglink']              # 可在setting中可以设置下载的路径
        yield scrapy.Request(img_link)          # 返回给引擎，它会给下载器下载

    def item_completed(self, results, item, info):
    # results的输出：
        #[(True, {'url': 'https://img3.doubanio.com/view/photo/s_ratio_poster/public/p480
        # 747492.jpg', 'path': 'full/07595a8bc272be84165d4a0e571a0bef6ff9c178.jpg', 'check
        # sum': 'e67af939b9b4475a3165413c0714c3a9'})]
        img_path = [x['path'] for ok, x in results if ok]   # why ?
        os.rename(img_store + img_path[0], img_store +'\\' + item['name'] + '.jpg')
        # print(img_store + img_path[0])
        # print(img_store + item['name'] + ',jpg')
