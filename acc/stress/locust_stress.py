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

# 登陆接口返回的token, 需要每次修改
token = ""

class QuickStartUser(HttpUser):
    wait_time = between(1, 1.5)
    host = 'https://www.acchw.top:9010'


    # @task
    # def version_info(self):
    #     """
    #     获取版本信息
    #     :return:
    #     """
    #     self.client.get("/acc/app/version")

    @task
    def add_detail(self):
        """
        添加明细
        """
        headers = {
            "Content-type": "application/json",
            "token": "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxNSIsImlhdCI6MTYzMTAwNDY2MCwiZXhwIjoxNjMzNTk2NjYwfQ.til6ivRLO1TiSjmW2ngYxgtOIwi8HeUXfTpQExEK0JgXKvIoAfDh2RSM60WlOT_o1kQGpSPGgNVZHHVzHuADIw"
        }
        t = datetime.now() + timedelta(random.randint(1, 200))
        data = {
            "uid": 15,
            "tid": 50210,
            "bid": 7,
            "amount": random.randint(1, 1000),
            "timeStamp": int(t.timestamp() * 1000)
        }
        res = self.client.post("/acc/app/detail/add", json=data, headers=headers)
        print("code=" + str(res.json()['code']))

    # def on_start(self):
    #     self.client.post("/login", json={"username":"foo", "password":"bar"})
