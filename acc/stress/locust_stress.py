"""
压力测试
locust -f locust_stress.py
"""

import time
from locust import HttpUser, task, between
from datetime import datetime, timedelta
import random

class QuickStartUser(HttpUser):
    wait_time = between(1, 1.5)
    host = 'http://10.171.7.45:9000'


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
        :return:
        """
        headers = {
            "Content-type": "application/json",
            "token": "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDEwMDAwMDA1IiwiaWF0IjoxNjIzODI0MDY4LCJleHAiOjE2MjY0MTYwNjh9.dxsTFS1UTVAW5SH1KJ0nM7KGfQWoL31Ioq6Cb81UpqhuYA_hk6GeXI779UR1P_ZamY2lq21FI2lsT_a-5t7jLQ"
        }
        t = datetime.now() + timedelta(random.randint(1, 200))
        data = {
            "uid": 1010000005,
            "tid": 1,
            "bid": 1,
            "amount": random.randint(1, 1000),
            "timeStamp": int(t.timestamp() * 1000)
        }
        res = self.client.post("/acc/app/detail/add", json=data, headers=headers)
        print("res=" + res.json()['code'])

    # def on_start(self):
    #     self.client.post("/login", json={"username":"foo", "password":"bar"})
