from tool import db

if __name__ == '__main__':
    sql = "insert into test.person(username, age, company_id) values (%s, %d, %d) "
    val = (('li', 'si', 16, 'F', 1000),
       ('Bruse', 'Jerry', 30, 'F', 3000),
       ('Lee', 'Tomcat', 40, 'M', 4000),
       ('zhang', 'san', 18, 'M', 1500))

    db_manger = db.MysqlHelper('10.171.7.45', '23306', 'root', '12358')
    db_manger.insert(sql)



