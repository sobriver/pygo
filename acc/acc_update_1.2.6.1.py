import mysql.connector
import json
import logging

if __name__ == '__main__':
    """
    将user_acc_type的所有sort值进行重新命名
    """

    # user_acc_type_1 extend 的值表示原先acc_type的id
    type_table = 'user_acc_type'

    conn = mysql.connector.connect(host="localhost", port='3306', user="root", passwd="12358", database="acc_app")
    cursor = conn.cursor()

    try:
        cursor.execute("select uid from " + type_table + " group by uid")
        uid_list = cursor.fetchall()
        for uid in uid_list:
            cursor.execute("select id from " + type_table + " where uid= %s and type =1 and extend is null order by id" % (uid))
            ids = cursor.fetchall()
            size = len(ids)
            if size > 0:
                for index, value in enumerate(ids):
                    sort = 11 + index
                    cursor.execute("update " + type_table + " set sort=%s where id=%s" % (sort, value[0]))
                    conn.commit()
                    print(f'{uid} update type 1 success')

            cursor.execute(
                "select id from " + type_table + " where uid= %s and type =2 and extend is null order by id" % (uid))
            ids2 = cursor.fetchall()
            size2 = len(ids)
            if size2 > 0:
                for index, value in enumerate(ids2):
                    sort = 10 + index
                    cursor.execute("update " + type_table + " set sort=%s where id=%s" % (sort, value[0]))
                    conn.commit()
                    print(f'{uid} update type 2 success')


    except Exception as e:
        logging.exception(e)
        conn.rollback()
