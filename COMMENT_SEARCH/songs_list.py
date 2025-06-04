import pymysql

def archive_songs_with_ranks(playlist_tables, archive_table):
    """
    将多个歌单表的数据归档到一个表中，并记录每首歌在不同榜单中的排名
    :param playlist_tables: 歌单表名列表
    :param archive_table: 归档表名
    """
    # 连接数据库
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="1234567890asd",
        database="music_samp",
        charset="utf8mb4",
    )
    try:
        cursor = conn.cursor()
        # 检查归档表是否存在
        cursor.execute(f"SHOW TABLES LIKE '{archive_table}'")
        if cursor.fetchone() is None:
            # 如果归档表不存在，创建表
            rank_columns = ", ".join([f"`{table}_rank` INT DEFAULT NULL" for table in playlist_tables])
            cursor.execute(f"""
                CREATE TABLE `{archive_table}` (
                    `id` INT AUTO_INCREMENT PRIMARY KEY,
                    `song_name` VARCHAR(255),
                    `singer` VARCHAR(255),
                    `link` VARCHAR(255),
                    {rank_columns},
                    UNIQUE(`song_name`, `singer`)
                )
            """)

        # 遍历每个歌单表，将数据插入归档表
        for table in playlist_tables:
            column_name = f"{table}_rank"
            cursor.execute(f"show columns from `{archive_table}` LIKE '{column_name}'")
            if cursor.fetchone() is None:
                cursor.execute(f"ALTER TABLE `{archive_table}` ADD COLUMN `{column_name}` INT DEFAULT NULL")
            cursor.execute(f"SELECT `rank`, `name`, `singer`, `link` FROM `{table}`")
            songs = cursor.fetchall()
            for song in songs:
                rank, name, singer, link = song
                # 插入或更新归档表
                cursor.execute(f"""
                    INSERT INTO `{archive_table}` (`song_name`, `singer`, `link`, `{table}_rank`)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE `{table}_rank` = VALUES(`{table}_rank`)
                """, (name, singer, link, rank))

        # 提交事务
        conn.commit()
        print("归档完成！")
    except pymysql.MySQLError as e:
        print(f"数据库错误: {e}")
    finally:
        cursor.close()
        conn.close()

# 示例调用
playlist_tables = ["新歌榜", "热歌榜", "飙升榜","原创榜"]  # 示例歌单表名
archive_table = "歌曲表"
archive_songs_with_ranks(playlist_tables, archive_table)