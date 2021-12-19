"""
locust压力测试
使用步骤：
1. 本地安装locust: pip install locust
2. 启动网页端: locust -f locust_stress.py
"""

import time
from locust import HttpUser, task, between
from datetime import datetime, timedelta
import random

# 接口服务地址
api_host = "http://10.171.7.45:9000"
# 登陆名
login_name = "sobriver"
# 密码
pwd = "123456"




class QuickStartUser(HttpUser):
    wait_time = between(1, 1.5)
    host = api_host


    def on_start(self):
        data = {
            "loginName": login_name,
            "password": pwd,
            "type": 1
        }
        res = self.client.post("/acc/app/user/login", json=data, headers={"Content-type": "application/json"})
        r_json = res.json()
        if r_json['code'] != 100000:
            print('login error, code:%d, msg:%s' % (r_json['code'], r_json['msg']))
            return
        print('---------------------------login success')
        self.token = r_json['data']['token']
        self.uid = r_json['data']['userInfo']['uid']
        self.headers = {
            "Content-type": "application/json",
            "token": self.token
        }
        type_res = self.client.get("/acc/app/acct/all/" + str(self.uid), headers=self.headers)
        type_res_json = type_res.json()
        if type_res_json['code'] != 100000:
            print('get type error, code:%d, msg:%s' % (type_res_json['code'], type_res_json['msg']))
            return
        self.type_list = []
        for item in type_res_json['data']:
            self.type_list.append(item['id'])
        print('-------------------------get type success type list:%d' % len(self.type_list))

        book_res = self.client.get("/acc/app/book/%d/default" % self.uid, headers=self.headers)
        book_res_json = book_res.json()
        if book_res_json['code'] != 100000:
            print('get book error, code:%d, msg:%s' % (book_res_json['code'], book_res_json['msg']))
            return
        self.bid = book_res_json['data']['id']
        print('------------------------get default book success, bid:%d' % self.bid)


    @task
    def add_detail(self):
        """
        添加明细
        """
        t = datetime.now() + timedelta(random.randint(1, 200))
        data = {
            "uid": self.uid,
            "tid": self.type_list[random.randint(0, len(self.type_list)-1)],
            "bid": self.bid,
            "amount": random.randint(1, 1000),
            "timeStamp": int(t.timestamp() * 1000)
        }
        res = self.client.post("/acc/app/detail/add", json=data, headers=self.headers)
        print("result code:%d msg:%s" % (res.json()['code'], res.json()['msg']))

