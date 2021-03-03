# coding=utf-8

import random
import logging.config
import requests
import os



def log():
    """
    测试logging模块
    :return: 
    """
    # 解决Windows下出现gbk的编码问题
    with open('test_logging.conf', encoding='utf-8') as file:
        logging.config.fileConfig(file)
        logger = logging.getLogger()

        logger.info('info test')
        logger.debug('debug test')
        logger.error('error test')
        logger.debug('thia')


def save():
    """
    测试下载图片到本地
    :return:
    """
def exception():
    for i in range(4):
        try:
            s = 6 / i
            print('i=' + str(i) + ' s=' + str(s))
        except Exception as e:
            print('exception execute')
            pass
        finally:
            print('finally execute')
def py():
    for i in range(20):
        print(i)








if __name__ == '__main__':
    for i in range(1, 5):
        print(i)