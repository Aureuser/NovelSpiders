# -*- coding: utf-8 -*-
'''
获取单个网页的html
'''
import requests
from Novels.setting import REQUEST_TIMEOUT,GET_PROXY_URL,REQUEST_HEADERS
from requests.exceptions import ConnectTimeout,ProxyError

get_proxy_url = GET_PROXY_URL
herders = REQUEST_HEADERS

def get_page(url,count=1):
    proxy = get_proxy()
    try:
        if proxy:
            r = requests.get(url=url,headers=herders,proxies=proxy,timeout=REQUEST_TIMEOUT)
        else:
            r = requests.get(url=url,headers=herders,timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            print("Get page successful:",url)
            return r.text
    except (ProxyError,ConnectTimeout) as e:
        if count > 3:
            print(url,'Try more than three times. Give up the experiment')
            return None
        print('Try again',count,url)
        get_page(url,count+1)
    except Exception:
        return None


def get_proxy():
    try:
        r = requests.get(url=get_proxy_url,timeout=REQUEST_TIMEOUT)
        if r.status_code == 200:
            return {'http://':'http://'+r.text}
        return None
    except Exception as e:
        return None

if __name__ == '__main__':
    html=get_page('http://www.jjxsw.com/e/action/newlist.php?page=0&class=2')
    print(html)