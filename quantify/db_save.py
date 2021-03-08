from datetime import datetime
import csv
import os
from clickhouse_driver import connect



def iter_csv(filename):
    """
    csv转换函数
    """
    list = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for item in reader:
            data = [
                datetime.strptime(item['date'], '%Y-%m-%d %H:%M:%S'),
                float(item['open']),
                float(item['high']),
                float(item['low']),
                float(item['close']),
                float(item['volume']),
                float(item['money']),
                float(item['open_interest']),
            ]
            list.append(data)
            # 每隔10000条提交一次
    return list




def save_all_bar(file):
    """
    保存所有csv数据
    """
    for dirpath, dirnames, filenames in os.walk(file):
        for filename in filenames:
            print(f'{str(datetime.now())} start {filename}')
            with open(os.path.join(dirpath, filename), 'r') as f:
                reader = csv.DictReader(f)
                list = []
                for item in reader:
                    data = [
                        datetime.strptime(item['date'], '%Y-%m-%d %H:%M:%S'),
                        float(item['open']),
                        float(item['high']),
                        float(item['low']),
                        float(item['close']),
                        float(item['volume']),
                        float(item['money']),
                        float(item['open_interest']),
                    ]
                    list.append(data)
                    # 每隔10000条提交一次
                    if len(list) == 10000:
                        save_data(list)
                        list.clear()
                save_data(list)

def save_data(list):
    cursor.executemany('insert into pqu(datetime, open, high, low, close, volume, money, open_interest) VALUES', list)
    conn.commit()
    print('提交10000成功')

conn = connect(host='10.171.17.20', port='8123', database='test')
cursor = conn.cursor()
if __name__ == '__main__':
    print(f'{str(datetime.now())} start')
    save_all_bar('D:\\test\pq1')
    print(f'{str(datetime.now())} end')

