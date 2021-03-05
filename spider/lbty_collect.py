import asyncio
import requests
from pyppet_util import PyppeteerBrowser
import sys
import os

if __name__ == '__main__':

    # 存储文件的路径
    file_path = 'D:\\test\\html'

    ppy = PyppeteerBrowser()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(ppy.getbrowser())
    loop.run_until_complete(ppy.open("https://robo.datayes.com", 60))
    page = loop.run_until_complete(ppy.getPage())
    cookie = loop.run_until_complete(ppy.getCookies(page))

    cookie_format = ''
    for item in cookie:
       cookie_format = cookie_format + str(item['name']) + '=' + str(item['value']) + ';'

    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit', 'cookie': cookie_format}
    r = requests.get('https://gw.datayes.com/rrp_mammon/web/feed/list', headers=headers)

    if r is None:
        print('无返回')
        sys.exit()


    result = r.json()
    data_list = []
    if result['code'] == 1:
        data = result['data']
        data_list = data['list']

    detail_ids = []
    for item in data_list:
        detail_ids.append(item['id'])

    for detail_id in detail_ids:
        article_ori = requests.get('https://gw.datayes.com/rrp_mammon/web/feed?id=' + str(detail_id), headers=headers)
        file_name = 'file_' + str(detail_id) + '.html'
        print(f'开始写入{file_name}')
        with open(os.path.join(file_path, file_name), mode='w', encoding='utf-8') as f:
            article_data = article_ori.json()['data']
            f.writelines('<html>')
            f.writelines('<head>')
            f.writelines('  <meta charset="utf-8">')
            f.writelines('</head>')
            f.writelines('<body>')
            f.write(article_data['longDocContent'])
            f.writelines('<body>')
            f.writelines('<html>')




