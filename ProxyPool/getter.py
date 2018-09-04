from ProxyPool.getpage import get_page
import re
from pyquery import PyQuery as pq
from lxml import etree

class ProxyMetaClass(type):
    def __new__(cls,name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)

class FreeProxyGetter(object,metaclass=ProxyMetaClass):
    def get_raw_proxies(self,callback):
        proxies = []
        try:
            for proxy in eval('self.{}()'.format(callback)):
                print('Getting', proxy, 'from', callback)
                #将返回的proxy代理添加到proxies列表里
                proxies.append(proxy)
        except:
            pass
        return proxies

    def crawl_kuaidaili(self):
        for page in range(1, 4):
            # 国内高匿代理
            start_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)
            html = get_page(start_url)
            ips = etree.HTML(html).xpath('//tbody/tr/td[@data-title="IP"]/text()')
            ports = etree.HTML(html).xpath('//tbody/tr/td[@data-title="PORT"]/text()')
            for adress, port in zip(ips,ports):
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_xicidaili(self):
        for page in range(1, 4):
            start_url = 'http://www.xicidaili.com/wt/{}'.format(page)
            html = get_page(start_url)
            ip_adress = re.compile(
                '<td class="country"><img src="http://fs.xicidaili.com/images/flag/cn.png" alt="Cn" /></td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>'
            )
            # \s* 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(html)
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_daili66(self, page_count=4):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_data5u(self):
        for i in ['gngn', 'gnpt']:
            start_url = 'http://www.data5u.com/free/{}/index.shtml'.format(i)
            html = get_page(start_url)
            ip_adress = re.compile(
                ' <ul class="l2">\s*<span><li>(.*?)</li></span>\s*<span style="width: 100px;"><li class=".*">(.*?)</li></span>'
            )
            # \s * 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(html)
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_kxdaili(self):
        for i in range(1, 4):
            start_url = 'http://www.kxdaili.com/ipList/{}.html#ip'.format(i)
            html = get_page(start_url)
            ip_adress = re.compile('<tr.*?>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s* 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(html)
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_premproxy(self):
        for i in ['China-01', 'China-02', 'China-03', 'China-04', 'Taiwan-01']:
            start_url = 'https://premproxy.com/proxy-by-country/{}.htm'.format(
                i)
            html = get_page(start_url)
            if html:
                ip_adress = re.compile('<td data-label="IP:port ">(.*?)</td>')
                re_ip_adress = ip_adress.findall(html)
                for adress_port in re_ip_adress:
                    yield adress_port.replace(' ', '')

    def crawl_xroxy(self):
        for i in ['CN', 'TW']:
            start_url = 'http://www.xroxy.com/proxylist.php?country={}'.format(
                i)
            html = get_page(start_url)
            if html:
                ip_adress1 = re.compile(
                    "title='View this Proxy details'>\s*(.*).*")
                re_ip_adress1 = ip_adress1.findall(html)
                ip_adress2 = re.compile(
                    "title='Select proxies with port number .*'>(.*)</a>")
                re_ip_adress2 = ip_adress2.findall(html)
                for adress, port in zip(re_ip_adress1, re_ip_adress2):
                    adress_port = adress + ':' + port
                    yield adress_port.replace(' ', '')

if __name__ == '__main__':
    fpg = FreeProxyGetter()
    fpg.get_raw_proxies('crawl_daili66')