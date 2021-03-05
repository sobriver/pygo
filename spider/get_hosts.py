# coding=utf-8

import os
from pyquery import PyQuery as pq
import requests
import pymysql
import re

"""
获取代理IP并进行检测,存入数据库中
"""


def get_ip():
    """
    获取代理IP并存入数据库
    :return:
    """
    isStop = False
    # 获取代理的网址
    url = 'http://www.xicidaili.com/nn/1'

    test_status_url = 'https://www.baidu.com'
    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0"}

    try:
        cursor, conn = conn_db()
        response = requests.get(url, headers=headers)
        content = pq(response.content)
        tr = content('#ip_list tr')
        for item in tr.items():
            host = item('td').eq(1).text()
            port = item('td').eq(2).text()
            address = item('td').eq(3).find('a').text()
            alive_time = item('td').eq(8).text()
            speed_ori = item('td').eq(6).find('div').attr('title')
            # 原文格式 0.79秒,转化成0.79
            speed = re.match('[0-9]+\.[0-9]+', str(speed_ori))
            if speed is not None:
                speed = speed.group()
            # 检验IP是否可用
            proxies = 'http://' + host + port
            status = requests.get(test_status_url, proxies=proxies).status_code
            if requests.codes.ok == status:
                try:
                    sql = "insert into ip(host, port, address, alive_time, speed) VALUES (%s, %s, %s, %s, %s)"
                    num = cursor.execute(sql, (host, port, address, alive_time, speed))
                    conn.commit()
                    print('写入数据库' + host + '成功')
                except Exception as e:
                    print(e)
                    print(host + "发生错误")

    finally:
        cursor.close()
        conn.close()




def conn_db():
    """
    创建数据库连接
    :return: 
    """
    # 数据库的配置
    host = '192.168.0.109'
    user = 'root'
    password = '12358'
    db_name = 'spider'
    # 创建数据库连接
    conn = pymysql.connect(host, user, password, db_name, charset='utf8')
    cursor = conn.cursor()
    return cursor, conn


if __name__ == '__main__':
    get_ip()
