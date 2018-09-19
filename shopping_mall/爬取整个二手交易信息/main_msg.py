# 主函数（爬取所有商品的信息）
from multiprocessing import Pool
from 网上商城.广州百姓网.爬取整个二手交易信息.spiders import goods_information, url_list, information_list

# urls_total = [data['url'] for data in url_list.find()]            # 如果爬取中出错，使用这块代码，找出出错后剩余未爬取的网址
# urls_ready = [data['url'] for data in information_list.find()]
# x = set(urls_total)                                               # 去除重复的url
# y = set(urls_ready)
# rest_of_urls = x - y                                              # 相减得到剩余未爬取的url

goods_urls = [goods_url['url'] for goods_url in url_list.find()]

if __name__ == '__main__':
    pool = Pool()
    pool.map(goods_information, goods_urls)      # 如果爬取中出现错误，将goods_urls改成rest_of_urls则可在出错的位置继续爬取，不必从新开始











