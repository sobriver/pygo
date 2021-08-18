"""
调用n次以图搜图接口并将结果写入excel
"""
import json
from PIL import Image
import requests
import xlsxwriter as xlsxwriter
import os
import uuid

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


if __name__ == '__main__':
    # 待搜索图片路径
    pic_path = r'D:\test\1000以脸搜脸\1000待搜索图片'
    # 写入excel路径
    excel_path = r'D:\test\1000以脸搜脸\data.xlsx'
    # 以图搜图接口
    search_url = 'http://10.171.4.205/v1/web/photo/search'
    # 上传图片接口
    upload_url = 'http://10.171.4.205/v1/web/person/config/upload_image'
    # 登陆token
    login_token = '39f11cd687bc40e5a1603f8f21ff2464'
    # 行宽
    width = 30
    # 行高
    height = 130
    # 搜索阈值
    threshold = 1
    # 库类型， 1 员工， 2 访客 3 重点人员 4 陌生人
    groupTypes = [1, 2, 3]

    # 临时文件存放路径
    tmp_path = r'D:\test\tmp'

    file_headers = {'login_token': login_token}
    search_headers = {'login_token': login_token, 'Content-Type': 'application/json;charset=UTF-8'}
    workbook = xlsxwriter.Workbook(excel_path)
    worksheet = workbook.add_worksheet()
    # 设置A, B, C, D 列宽度
    worksheet.set_column('A:A', width)
    worksheet.set_column('B:B', width)
    worksheet.set_column('C:C', width)
    worksheet.set_column('D:D', width)

    for pre_index, pic in enumerate(os.listdir(pic_path)):
        print('-----------start search %s %d' % (pic, pre_index))
        # 获取图片uri
        files = {'file': open(os.path.join(pic_path, pic), 'rb')}
        file_re = requests.post(upload_url, files=files, headers=file_headers)
        if not file_re.ok:
            print('upload file error')
            continue
        file_json = file_re.json()
        if file_json['code'] != 0:
            print('upload file fail %s' % (file_json['msg']))
            continue
        search_file_uri = file_json['data']['uri']

        data = {
            "uri": search_file_uri,
            "zoneId": 1,
            "threshold": threshold,
            "pageNum": 1,
            "pageSize": 3,
            "groupTypes": groupTypes
        }
        re = requests.post(search_url, data=json.dumps(data), headers=search_headers)
        if not re.ok:
            print('search error %s' % (data))
            continue
        search_json = re.json()
        if search_json['code'] != 0:
            print('upload file fail %s' % (search_json['msg']))
            continue
        search_data_list = search_json['data']['list']
        if search_data_list is None or len(search_data_list) == 0:
            print('not match photo')
            continue
        print('match photo size:%d' % (len(search_data_list)))

        # 设置行的高度
        worksheet.set_row(pre_index, height)
        tmp1 = os.path.join(tmp_path, str(uuid.uuid1()) + '.jpg')
        resize_image(os.path.join(pic_path, pic), tmp1)
        worksheet.insert_image(pre_index, 0, tmp1)
        for index, item in enumerate(search_data_list):
            pic_data = requests.get(item['url'])
            tmp2 = os.path.join(tmp_path, str(uuid.uuid1()) + '.jpg')
            with open(tmp2, 'wb') as f:
                f.write(pic_data.content)
            tmp3 = os.path.join(tmp_path, str(uuid.uuid1()) + '.jpg')
            resize_image(tmp2, tmp3)
            worksheet.insert_image(pre_index, index+1, tmp3)
            worksheet.write(pre_index, index+1, item['score'])

    workbook.close()
    # 删除临时文件
    del_list = os.listdir(tmp_path)
    for f in del_list:
        file_path = os.path.join(tmp_path, f)
        if os.path.isfile(file_path):
            os.remove(file_path)










