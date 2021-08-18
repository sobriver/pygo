import requests
import xlsxwriter
import json
from PIL import Image
import os

web_ip = 'http://10.171.4.205'
token = '39f11cd687bc40e5a1603f8f21ff2464'
face_ids = []
xls_file = r'D:\test\export_pro.xlsx'
# 行宽
width = 30
# 行高
height = 130

def resize_image(old_img, new_img, width=150, height=150):
    """
    缩放图片大小到固定尺寸
    :param old_img: 原图
    :param new_img: 新图
    :param width: 宽度
    :param height: 高度
    """
    try:
        img = Image.open(old_img)
        tmp_img = img.resize((width, height), Image.BILINEAR)
        tmp_img.save(new_img)
    except Exception as e:
        print(e)
        pass


def get_profiles():
    url = "{}/v1/web/person/high/record/list".format(web_ip)
    # url='http://10.171.4.205/v1/web/person/high/record/list'
    data = {"pageNum":1,"pageSize":2000,"personName":"","count":"","orderReq":{"filed":"latestTime","order":"desc"},"zoneIds":["1"]}
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'login_token':token
    }
    r = requests.post(url=url, data=json.dumps(data), headers=headers)
    ret = json.loads(r.content.decode('utf-8'))
    print(ret)
    profiles = ret.get('data', {}).get('list',[])
    return profiles

def get_pro_detail(p_id):
    url = "{}/v1/web/person/high/record/detail".format(web_ip)
    # url='http://10.171.4.205/v1/web/person/high/record/list'
    data = {"pageNum":1,"pageSize":60,"personId":p_id,"deviceIds":[],"zoneId":"1","startTime":1626710400000,"endTime":1629302400000}
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json, text/plain, */*',
        'login_token': token
    }
    r = requests.post(url=url, data=json.dumps(data), headers=headers)
    ret = json.loads(r.content.decode('utf-8'))
    # print(ret)
    captures = ret.get('data', {}).get('list', [])
    print(captures)
    return captures

def get_img_data(url):
    res = requests.get(url.strip())
    data = res.content
    return data

def write_pro2excel(profiles):
    workbook = xlsxwriter.Workbook(xls_file)
    worksheet = workbook.add_worksheet()
    # worksheet.insert_image(0, 0, 'tmp.jpg')
    worksheet.set_column('A:A', width)
    # worksheet.set_column('B:B', width)
    # worksheet.set_column('C:C', width)
    # worksheet.set_column('D:D', width)
    worksheet.set_column('E:E', width)
    worksheet.set_column('F:F', width)
    i=0
    print('len==========%d' % len(profiles))
    for pro in profiles:
        print('i===============%d' % i)
        group_img_url = pro.get('groupImageUrl', '')
        personName = pro.get('personName', '')
        count=pro.get('count', '')
        zoneName=pro.get('zoneName', '')
        personId=pro.get('personId', '')

        face_path = './tmp/diku_{}.jpg'.format(i)
        file0 = open(face_path, 'wb')
        file0.write(get_img_data(group_img_url))
        file0.close()

        face_tmp_path='./tmp/tmp_diku_{}.jpg'.format(i)
        resize_image(face_path, face_tmp_path)

        worksheet.set_row(i, height)
        worksheet.insert_image(i, 0, face_tmp_path)
        worksheet.write(i, 1, personName)
        worksheet.write(i, 2, count)
        worksheet.write(i, 3, zoneName)

        captures=get_pro_detail(personId)
        j=4
        for capture in captures:
            captureImageUrl=capture.get('captureImageUrl','')
            score = capture.get('score', '')

            cap_path = './tmp/cap_{}_{}.jpg'.format(i,j)
            file1 = open(cap_path, 'wb')
            file1.write(get_img_data(captureImageUrl))
            file1.close()

            cap_tmp_path = './tmp/tmp_cap_{}_{}.jpg'.format(i,j)
            resize_image(cap_path, cap_tmp_path)

            worksheet.insert_image(i, j, cap_tmp_path)
            j=j+1

        i = i + 1
    workbook.close()






if __name__ == '__main__':
    profiles = get_profiles()
    write_pro2excel(profiles)

    # captures=get_pro_detail("220813")
