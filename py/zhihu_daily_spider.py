# coding=utf-8

# 爬虫知乎日报

import requests


def get():
    url = 'http://daily.zhihu.com/'
    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0"}
    proxies = {
        "http": "http://119.5.0.80:808",
        "https": "http://115.220.150.198:808",
    }
    code = requests.get(url, headers=headers, proxies=proxies).status_code
    print(code)


if __name__ == '__main__':
    get()
