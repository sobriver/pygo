"""
压力测试
locust -f locust_stress.py
"""

import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)
    host = 'http://10.171.7.45:9000'

    @task
    def hello_world(self):
        self.client.get("/acc/app/t_uyyy/t1")

    # def on_start(self):
    #     self.client.post("/login", json={"username":"foo", "password":"bar"})