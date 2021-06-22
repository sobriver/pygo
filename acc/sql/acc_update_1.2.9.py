import json

import mysql.connector
import logging
import os,base64
import requests


def run():
    """
       1.2.9版本更新脚本
       """
    # 文件保存路径
    s_path = 'D:\\tmp\\fdfd1'
    # 上传图片
    upload_url = 'http://10.171.7.45:9000/acc/app/file/upload/pic'
    edit_url = 'http://10.171.7.45:9000/acc/app/detail/edit'
    token = 'eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJzdWIiOiIxMDEwMDAwMDA1IiwiaWF0IjoxNjIzMzk5NTQyLCJleHAiOjE2MjU5OTE1NDJ9.Qj1lwg1S4g2d1eBkZdpfsatMH32J0riVL7krIGTFt0Ao7L8-ObHcgq9cLqm1O5BYOz-AZHwRYPG8ekmj6_mywg'
    headers = {
        'token': token,
    }
    headers1 = {
        'token': token,
        'Content-Type': 'application/json'
    }
    detail_table = 'acc_detail'

    conn = mysql.connector.connect(host="10.171.7.45", port='3306', user="root", passwd="huang1320", database="acc_app")
    cursor = conn.cursor()
    try:
        cursor.execute("select id, pic_content from acc_detail where tna_pic is not null and pic_content is not null")
        datas = cursor.fetchall()
        for data in datas:
            id = data[0]
            pic_content = data[1]

            imgData = base64.b64decode(pic_content)
            f_name = str(id) + '.jpg'
            p = os.path.join(s_path, f_name)
            with open(p, 'wb') as f:
                f.write(imgData)
            print("生成文件成功：" + p)
            files = {'file': open(p, 'rb')}
            r = requests.post(upload_url, files=files, headers=headers)
            js = r.json()
            if js['code'] != 100000:
                print('失败 ' + str(js))
                continue
            uri = js['data']['uri']
            rData = {
                "id": id,
                "picUri": uri
            }
            re1 = requests.post(edit_url, data=json.dumps(rData), headers=headers1)
            print('id:%s uri:%s re1:%s' % (str(id), uri, str(re1.json())))



    except Exception as e:
        logging.exception(e)
        conn.rollback()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    run()