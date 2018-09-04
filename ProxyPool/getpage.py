import requests
import time
def get_page(url,other={}):
    base_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    headers = dict(base_headers,**other)
    try:
        time.sleep(3)
        r = requests.get(url,headers=headers)
        print('Getting result', url, r.status_code)
        if r.status_code == 200:
            return r.text
    except:
        print('Crawling Failed', url)
        return None
