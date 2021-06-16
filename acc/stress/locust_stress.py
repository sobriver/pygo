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
            "token": "eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDEwMDAwMDA1IiwiaWF0IjoxNjIzODI2MzkwLCJleHAiOjE2MjY0MTgzOTB9.OdaxCUL6NO_22DV-_RJM-xsLwoktH7Ngiws3JIkw0jIbr-pk6ZPMCz2NbJXOmKBoHCMgHHqzl11-cvoe6OB7KA"
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
        print("res=" + str(res.json()['code']))

    # def on_start(self):
    #     self.client.post("/login", json={"username":"foo", "password":"bar"})
