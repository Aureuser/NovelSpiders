# -*- coding: utf-8 -*-
'''
获取小说网站中的小说txt文件
'''
from Novels.getpage import get_page
from lxml import etree
import pymongo
from Novels.db import MongoClient
from Novels.setting import MONGO_PORT,MONGO_HOST
class NovelSpiderMethod(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__Crawl'] = []
        for key,value in attrs.items():
            if key.startswith('crawl'):
                attrs['__Crawl'].append(key)
                count+=1
        attrs['__CrawlCount'] = count
        return type.__new__(cls, name, bases, attrs)


class NovelSpider(object,metaclass=NovelSpiderMethod):
    def __init__(self):
        self._db = MongoClient()


    def get_novels(self,callback):
        novels = []
        for novel in eval('self.{callback}()'.format(callback=callback)):
            print('Getting', novel, 'from', callback)
            print(self._db.insert_one(novel))
        return novels

    def crawl_jjxsw(self):
        base_url = 'http://www.jjxsw.com/e/action/newlist.php?page={}&class={}'
        for url_class in range(1,4):
            url = base_url.format(0,url_class)
            html = get_page(url)
            # print(html)
            # 判断html类型是否为str避免发生ValueError
            if isinstance(html,str):
                r = etree.HTML(html)
                next_page = r.xpath('//div[@class="pager"]/ul/a/b/text()')[0]
                list_urls = [base_url.format(page,url_class) for page in range(0,int(next_page)//10+1)]
                for list_url in list_urls:
                    html = get_page(list_url)
                    r = etree.HTML(html)
                    novel_urls = r.xpath('//span[@class="title"]/a/@href')
                    for novel_url in novel_urls:
                        novel_url = 'http://www.jjxsw.com'+novel_url
                        html = get_page(novel_url)
                        if isinstance(html,str):
                            # 分析html，提取小说信息
                            yield self.parse_jjxsw(html).__next__()




    def parse_jjxsw(self,html):
        r = etree.HTML(html)
        item = dict()
        # 名字
        item['name'] = r.xpath('//div[@id="downInfoArea"]/h1/text()')
        # 作者
        item['auther'] = r.xpath('//div[@class="downInfoRowL"]/li[@class="zuozhe"]/a/text()')
        # 书籍分类
        item['classification'] = r.xpath('//div[@class="downInfoRowL"]/li[2]/text()')
        # 书籍大小
        item['size'] = r.xpath('//div[@class="downInfoRowL"]/li[3]/text()')
        # 书籍类型
        item['type'] = r.xpath('//div[@class="downInfoRowL"]/li[4]/text()')
        # 进度
        item['progress']  = r.xpath('//div[@class="downInfoRowL"]/li[6]/span/text()')
        # 上传者
        item['uploader'] = r.xpath('//div[@class="downInfoRowL"]/li[7]/a/text()')
        # 更新时间
        item['time'] = r.xpath('//div[@class="downInfoRowL"]/li[8]/text()')
        yield item


    def crawl_txt53(self):
        base_url = 'http://www.txt53.com/'

    def crawl_bookban(self):
        base_url = 'https://www.bookben.net/'

    def crawl_xiashu(self):
        base_url = 'https://www.xiashu.la/'

    def crawl_qisuu(self):
        base_url = 'https://www.qisuu.la/'

    def crawl_bookbaow(self):
        base_url = 'https://www.bookbaow.com/'

    def crawl_qishu(self):
        base_url = 'http://www.qishu.cc/'

if __name__ == '__main__':
    ns = NovelSpider()
    n = ns.get_novels('crawl_jjxsw')