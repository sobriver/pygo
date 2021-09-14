from datetime import datetime, timedelta
import subprocess
from loguru import logger
import os
import zipfile
import shutil
import pymysql

logger.add('timer.log', level='INFO', format='[{time:YYYY-MM-DD HH:mm:ss}-{file}-{line}] {message}', rotation="30 MB")


def clear_request_log():
    db_host = '10.171.7.45'
    db_port = 23306
    db_user = 'root'
    db_pwd = '12358'
    conn = pymysql.connect(host=db_host, port=db_port, user=db_user, passwd=db_pwd, database='test', charset='utf8')
    cursor = conn.cursor()
    try:
        dt1 = datetime(2021, 9, 10)
        dt2 = datetime(2021, 9, 15)
        rows = cursor.execute("select count(*) from person where gmt_create >= %s and %s" % (dt1, dt2))
        # conn.commit()
        print(cursor.fetchone())
    except Exception as e:
        logger.error(e)
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    clear_request_log()

