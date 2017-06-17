# coding=utf-8

import requests
from pyquery import PyQuery as pq
import time
import os
from py.utils.logger_utils import Logger

# 爬取斗图啦网站https://www.doutula.com所有图片,下载至本地

def get_pic():

    # 总页数
    total = 844
    base_url = 'https://www.doutula.com/photo/list/?page='
    page = range(1, total+1)

    for url in page:
        url = base_url + str(url)
        headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0"}
        # 每次休眠4秒再请求
        time.sleep(4)
        logger.debug('本次请求地址=' + url)
        response = requests.get(url, headers=headers)
        content = pq(response.content)
        pic_list = content('#pic-detail .row .col-sm-9 .page-content .col-xs-4')
        logger.debug('本次图片数量=' + str(len(pic_list)))
        for item in pic_list.items():
            try:
                pic = item('img')
                # 动态图片
                if pic.eq(0).has_class('gif'):
                    pic_src = pic.eq(1).attr('data-original')
                    pic_name = pic.eq(1).attr('alt')
                    save(pic_name, pic_src)
                # 静态图片
                else:
                    pic_src = pic.attr('data-original')
                    pic_name = pic.attr('alt')
                    save(pic_name, pic_src)
            except Exception as e:
                logger.error(e)
                pass




def save(name, url, path):
    """
    保存图片到本地
    @:param name 图片文件名
    @:param url  图片的请求地址
    @:param path 保存图片的本地路径
    :return:
    """
    # 得到图片文件的后缀
    url_data = str(url).split('.')
    suffix = url_data[len(url_data)-1]
    url = 'http:' + url
    filename = path + os.sep + name + '.' + suffix
    # 请求图片
    try:
        resp = requests.get(url)
        with open(filename, 'wb') as img:
            img.write(resp.content)
            logger.debug(str(filename) + '下载成功')
    except Exception as e:
        logger.error(str(filename) + '下载失败')
        logger.error(e)
        pass


if __name__ == '__main__':
    logging_conf = './conf/get_pic_logging.conf'
    logger = Logger(logging_conf).getLogger()

    # 保存图片的本地路径
    path = 'E:\pic'
    get_pic()
