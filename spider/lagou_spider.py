

from pyquery import PyQuery as pq
import requests
import pymysql





def get_company():
    """
    获取公司信息
    :return: 
    """
    file_path = '/Users/hw/spider/company.txt'
    url = 'https://www.lagou.com/gongsi/0-0-0'
    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:52.0) Gecko/20100101 Firefox/52.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != requests.codes.ok:
        print("响应服务器错误")
        return
    content = pq(response.content)
    companys = content('#company_list .item_con_list li')

    if len(companys) == 0:
        print("公司列表为空")
        return
    f = open(file_path, 'a')
    for item in companys.items():
        # 公司名称
        name = item('.item_cont .fr h3 a').text()
        # 公司详情页面地址
        details_url = item('.item_cont .fr h3 a').attr('href')
        # 评价该公司面试情况地址
        details_evaluate_url = item('.item_cont .fr .sub_title p').eq(0).find('a').attr('href')
        # 公司简介
        info = item('.item_cont .details p').text()
        # 公司类别
        type = item('.company_state span').eq(0).attr('title')
        # 公司地址
        address = item('.company_state span').eq(1).attr('title')
        # 融资阶段
        finance = item('.company_state span').eq(2).attr('title')

        f.write(name + '\t' + info + '\t' + details_url + '\n')
        print("写入==>" + name + "<==成功")

    f.close()

def connect_db():
    config = {
        'host': '192.168.1.168',
        'port': '3306',
        'user': 'root',
        'password': '12358',
        'db': 'lagou',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
    }
    


if __name__ == '__main__':
    get_company()


