from clickhouse_driver import connect

if __name__ == '__main__':
    conn = connect('clickhouse://10.171.17.20:8123')
    cursor = conn.cursor()
    sql = 'insert into test.pqu(datetime, open, high, low, close, volume, money, open_interest) VALUES'
    cursor.executemany(sql, [['2020-01-02 12:30:30', 12.43, 12.21, 12.21, 12.21, 12.21, 12.21, 12.21]])
    conn.commit()
    cursor.close()
    conn.close()
