import mysql.connector
import json
import logging



if __name__ == '__main__':
    """
    1.2.6版本数据库脚本， 用于acc_type重构
    """


    # user_acc_type_1 extend 的值表示原先acc_type的id
    detail_table = 'acc_detail_1'
    timer_table = 'add_detail_timer_1'
    type_table = 'user_acc_type_1'

    conn = mysql.connector.connect(host="localhost", port='3306', user="root", passwd="12358", database="acc_app")
    cursor = conn.cursor()
    try:
        # 得到uid
        cursor.execute("select uid from app_user")
        uid_list = cursor.fetchall()

        for uid in uid_list:
            # 将所有系统类别插入
            cursor.execute("insert into " + type_table + " (extend, type, name, description, icon, color, sort, uid) "
                           "select id, type, name, description, icon, color, sort, %s from acc_type" % (uid))
            conn.commit()
            print('类别插入完成')

        # 查询acc_detail中是否有sys tid的记录
        cursor.execute("select uid, tid from " + detail_table + " group by uid, tid")
        uid_tid_list = cursor.fetchall()
        if len(uid_tid_list) > 0:
            for uid_tid in uid_tid_list:
                cursor.execute("select id from " + type_table + " where uid=%s and extend=%s" % (str(uid_tid[0]), str(uid_tid[1])))
                s = cursor.fetchone()
                if s is None:
                    continue
                new_tid = s[0]
                rows = cursor.execute("update " + detail_table + " set tid = %s where uid=%s and tid=%s" % (str(new_tid), str(uid_tid[0]), str(uid_tid[1])))
                conn.commit()
                print("更新detail记录数：" + str(uid_tid))

        # 查询add_timer_detail中是否有sys tid的记录
        cursor.execute("select uid, tid from " + timer_table + " group by uid, tid")
        uid_tid_list2 = cursor.fetchall()
        if len(uid_tid_list2) > 0:
            for uid_tid in uid_tid_list2:
                cursor.execute(
                    "select id from " + type_table + " where uid=%s and extend=%s" % (str(uid_tid[0]), str(uid_tid[1])))
                s = cursor.fetchone()
                if s is None:
                    continue
                new_tid = s[0]
                rows = cursor.execute("update " + timer_table + " set tid = %s where uid=%s and tid=%s" % (
                str(new_tid), str(uid_tid[0]), str(uid_tid[1])))
                conn.commit()
                print("更新timer记录数：" + str(uid_tid))

        # todo 排序规则暂时不管了，就这样吧
    except Exception as e:
        logging.exception(e)
        conn.rollback()

    cursor.close()
    conn.close()