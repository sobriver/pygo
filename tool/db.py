import pymysql

class MysqlHelper:

    def __init__(self, host, port, username, pwd):
        self.db = pymysql.connect(host, port, username, pwd)
        self.cursor = self.db.cursor()

    def insert(self, sql):
        """
        单条插入
        """
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
        self.close()

    def batch_insert(self, sql):
        """
        批量插入
        """
        try:
            self.cursor.executemany(sql)
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
        self.close()

    def close(self):
        self.cursor.close()
        self.db.close()