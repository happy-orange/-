# 主函数（爬取所有商品的url）
# 待完善：爬取中因出错而停止，如何从出错后的地方继续爬取

from multiprocessing import Pool
from 网上商城.广州百姓网.爬取整个二手交易信息.spiders import goods_links_page, url_list, information_list
from 网上商城.广州百姓网.爬取整个二手交易信息.links_class_total import links_class_total


def put_links(link_class):
    for page in range(1, 101):                           # 用循环把页码也添加到spider1里的函数中
        goods_links_page(link_class, page)


if __name__ == '__main__':
    pool = Pool()                     # 这里有个默认参数process(进程)，不填是最好的，会根据电脑的cpu核数自动分配
    pool.map(put_links, links_class_total.split())          # 把之前爬取的所有二手货分类的网址逐一塞进put_links中









