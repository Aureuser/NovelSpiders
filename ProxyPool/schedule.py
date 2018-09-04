import time
from ProxyPool.getter import FreeProxyGetter
from ProxyPool.setting import TEST_API,PROXY_MAX,PROXY_MIN,CYCLE_TIME
from ProxyPool.db import RedisClient
import requests
import threadpool
from multiprocessing import Process
import pymongo

class ValidityTester():
    test_api = TEST_API
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400'}

    def __init__(self):
        self.test_proxies = []

    def set_test_procies(self,proxies):
        self.test_proxies = proxies
        self.conn = RedisClient()

    def test_single_proxy(self,proxy):
        try:
            if isinstance(proxy,bytes):
                proxy = proxy.decode('utf-8')
            real_proxy = 'http://'+proxy
            r = requests.get(url=self.test_api,proxies={'http://':real_proxy},headers=self.header)
            if r.status_code == 200:
                self.conn.put(proxy)
                print('验证成功：',proxy)
            else:
                print('验证失败：',proxy)
        except:
            print('请求失败：',proxy)

    def test(self):
        try:
            test_proxy_pool = threadpool.ThreadPool(5)
            test_proxy_requests = threadpool.makeRequests(self.test_single_proxy,self.test_proxies)
            for tpr in test_proxy_requests:
                test_proxy_pool.putRequest(tpr)
            test_proxy_pool.wait()
            self.test_proxies = []
        except:
            self.test()

class PoolAdder(object):
    def __init__(self):
        self.proxy_max = PROXY_MAX
        self.tester = ValidityTester()
        self.getter = FreeProxyGetter()
        self.conn = RedisClient()

    def is_picture(self):
        if self.conn.count() < self.proxy_max:
            return True
        return False

    def add_to_redis(self):
        proxy_count = 0
        while self.is_picture():
            for callback_label in range(self.getter.__CrawlFuncCount__):
                callback = self.getter.__CrawlFunc__[callback_label]
                raw_proxies = self.getter.get_raw_proxies(callback)
                self.tester.set_test_procies(raw_proxies)
                self.tester.test()
                proxy_count += len(raw_proxies)
                if not self.is_picture():
                    print('代理ip队列已满')
                    break
            if proxy_count == 0:
                print('请求不到ip')
                break


class Schedule(object):

    @staticmethod
    def control_add_proxy():
        proxy_min = PROXY_MIN
        conn = RedisClient()
        addr = PoolAdder()
        cycle = CYCLE_TIME
        while True:
            if conn.count() < PROXY_MAX:
                addr.add_to_redis()
            time.sleep(cycle)

    @staticmethod
    def control_test_proxy():
        conn = RedisClient()
        cycle = CYCLE_TIME
        tester = ValidityTester()
        while True:
            print('Refreshing ip')
            count = int(0.5 * conn.count())
            if count == 0:
                print('Waiting for adding')
                time.sleep(cycle)
                continue
            raw_proxies = conn.get(count)
            tester.set_test_procies(raw_proxies)
            tester.test()
            time.sleep(cycle)

    def run(self):
        Process(target=Schedule.control_add_proxy).start()
        Process(target=Schedule.control_test_proxy).start()

if __name__ == '__main__':
    # r = requests.get(url=TEST_API,proxies={"http": 'http://140.143.164.107:8888'},headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400'})
    # print(r.status_code)
    Schedule().run()