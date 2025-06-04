import pymysql
#实现可以分批次处理的函数，传递参数包括一次处理的行数和数据表名
def manageData(data_deque, table_name, columns):
    # 连接数据库
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='1234567890asd',
                           database='music_samp',
                           charset='utf8mb4')
    try:
        cursor = conn.cursor()
        # 检查表是否存在
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        if cursor.fetchone() is None:
            # 如果表不存在，创建表
            colums_defination = ','.join([f"`{col}` VARCHAR(255)" for col in columns])
            cursor.execute(f"CREATE TABLE `{table_name}` ({colums_defination})")
            cursor.execute(f"INSERT INTO `tables_name` (`name`) VALUES ('{table_name}')")
        # 批量插入数据
        columns_str = ', '.join([f"`{col}`" for col in columns])  # 用反引号括住列名
        placeholders = ', '.join(['%s'] * len(columns))  # 占位符
        sql = f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({placeholders})"
        cursor.executemany(sql, data_deque)
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        # 提交事务
        conn.commit()
        # 关闭游标和连接
        cursor.close()
        conn.close()
def manage_data_deque(data_deque,table_name,columns):
    #分批次处理
    batch_size = 1000
    while data_deque:
        #获取当前批次数据
        batch_data = [data_deque.popleft() for _ in range(min(batch_size, len(data_deque)))]
        #处理数据
        manageData(batch_data,table_name,columns)
        #清空当前批次数据
        batch_data.clear()
        #释放内存
        del batch_data
        #打印当前批次数据处理完成
        print(f"当前批次数据处理完成，剩余数据：{len(data_deque)}")
        #检查是否还有数据
        if len(data_deque) == 0:
            print("所有数据处理完成")
            break







