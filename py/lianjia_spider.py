#coding=utf-8
import requests
from pyquery import PyQuery as pq
import logging
import pymysql

def get():
    """
    暂时先考虑北京地区
    :return: 
    """
    conn, cursor = init_db()


    ori_url = 'http://bj.lianjia.com/zufang/'
    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0"}
    # 总页数,一般情况下为100
    num_page = 100

    url_list = []
    # 将所有页面的URL存入列表中
    for item in range(1, num_page + 1):
        url = ori_url + 'pg' + str(item) + '/'
        url_list.append(url)
    logging.debug('页面总数' + str(len(url_list)))



    # 对所有页面进行请求
    for item in url_list:
        response = requests.get(item, headers=headers)
        if response.status_code == requests.codes.ok:
            logging.debug('请求' + item + '成功')
            # 解析页面






        else:
            logging.error('请求' + item + '失败')
            continue




def init_log():
    """
    初始化日志,同时输出到文件和控制台
    :return: 
    """
    log_file = '/Users/hw/log.log'
    form = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'
    logging.basicConfig(filename=log_file, level=logging.DEBUG,
                        format=form,
                        datefmt='%a, %d %b %Y %H:%M:%S')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(form)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def init_db():
    """
    初始化数据库
    :return: conn,cursor
    """
    host = '192.168.1.168'
    user = 'root'
    password = '12358'
    db_name = 'spider'
    conn = pymysql.connect(host, user, password, db_name)
    cursor = conn.cursor()
    return conn, cursor











if __name__ == '__main__':
    init_log()
