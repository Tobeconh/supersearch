import pymysql
#实现可以分批次处理的函数，传递参数包括一次处理的行数和数据表名
def manageData(data_deque, table_name, columns):
    #连接数据库
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='1234567890asd',
                           database='music_samp',
                           charset='utf8mb4')
    try:
        cursor = conn.cursor()
        """将deque中的数据批处理进入数据库"""
        cursor.execute(f"SHOW TABLES LIKE {table_name}")
        #检查表是否存在
        if cursor.fetchone() is None:
            #如果表不存在，创建表
            cursor.execute(f"CREATE TABLE {table_name} ({columns})")
            cursor.execute(f"INSERT INTO `tables_name` (`name`) VALUES ('{table_name}')")
        #批量插入数据
        placeholders = ', '.join(['%s'] * len(columns.split(',')))

        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        # %s表示占位符
        #将元祖数据插入到数据库中
        cursor.executemany(sql, data_deque)
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        #提交事务
        conn.commit()
        #关闭游标和连接
        cursor.close()
        conn.close()







