# -*- coding: utf-8 -*-
import scrapy
from douban_films_top250.items import DoubanFilmsTop250Item


class FilmSpider(scrapy.Spider):
	name = 'film'
	allowed_domains = ['movie.douban.com']
	base_url = 'https://movie.douban.com/top250?start='
	offset = 0
	start_urls = [base_url + str(offset)]

	def parse(self, response):
		msgs = response.css('ol li')

		# 用来存储所有的item字段
		# items = []
		for msg in msgs:
			# 创建item字段对象，用来存储信息
			item = DoubanFilmsTop250Item()
			name = msg.css('.hd a span::text').extract()
			message = msg.css('.bd p::text').extract()
			score = msg.css('.rating_num::text').extract()
			abstract = msg.css('.inq::text').extract()
			imglink = msg.css('img::attr(src)').extract()

			item['name'] = name[0]
			item['message'] = message[0]
			item['score'] = score[0]
			item['abstract'] = abstract[0]
			item['imglink'] = imglink[0]
			# items.append(item)
			yield item
		# 换页(拼接url)
		if self.offset < 50:
			self.offset += 25
			url = self.base_url + str(self.offset)
			# Request是源码中的一个方法，用于请求url，参数callback用于将新的url回调给parse方法
			yield scrapy.Request(url, callback=self.parse)

		# 换页(提取下页url)
		# url = response.css('span.next a::attr(href)').extract()
		# if url:
		# 	# print('https://movie.douban.com/top250' + url[0])
		# 	yield scrapy.Request('https://movie.douban.com/top250' + url[0], callback=self.parse)


		# 返回给引擎（再由引擎返回给管道）
		# return items

