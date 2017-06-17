# coding=utf-8
import pymysql
import requests
import random
import time
import logging.config

# 获取熊猫金库的内容

def get():
    # url = 'http://www.xiongmaojinku.com/web/livedata'
    url = 'http://www.xiongmaojinku.com/web/data'
    header= [{'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0"},
             {'User-Agent':"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1"},
             {'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1;360SE)"},
             {'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1;Maxthon 2.0)"}]
    headers = header[random.randint(0, len(header) - 1)]
    try:
        cursor, conn = conn_db()
        response = requests.get(url, headers=headers, timeout=60)
        if response.status_code == requests.codes.ok:
            json_data = response.json()
            total_free = json_data['data']['trade']
            total_user = json_data['data']['register']
            year_rate = json_data['data']['rate_map'][0]['rate']
            sql = "insert into xiongmao(total_free,  total_user,year_rate ) VALUES (%s, %s, %s)"
            logger.debug('获得数据成功, total_free=' + str(total_free) + 'total_user=' + total_user)
            try:
                cursor.execute(sql, (str(total_free), total_user, year_rate))
                conn.commit()
            except Exception as e:
                conn.rollback()
                logger.error('插入数据库失败')
                logger.error(e)
        else:
            logger.error('访问网络失败, 返回码=' + response.status_code)
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
    try:
        conn = pymysql.connect(host=host,
                               user=user,
                               password=password,
                               db=db_name,
                               charset='utf8')
        cursor = conn.cursor()
        return cursor, conn
    except Exception as e:
        logger.error('数据库连接失败')
        logger.error(e)

if __name__ == '__main__':
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger()
    # 在每个小时的头15分钟随机取一个分钟执行脚本
    t = random.randint(0, 15 * 60)
    time.sleep(t)
    logger.debug('本次休眠时间[' + str(t) + ']')
    get()