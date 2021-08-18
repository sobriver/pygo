import pymysql

def get_connection():
    host = '192.168.0.109'
    user = 'root'
    password = '12358'
    db_name = 'spider'
    # 创建数据库连接
    conn = pymysql.connect(host, user, password, db_name, charset='utf8')
    cursor = conn.cursor()
    return cursor, conn

dbManger = get_connection()