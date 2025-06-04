import time
import requests
import pymysql
import json
import random

def generate_random_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    ]
    accept_languages = [
        "en-US,en;q=0.9",
        "zh-CN,zh;q=0.9",
        "en-GB,en;q=0.8",
        "zh-TW,zh;q=0.7",
    ]
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": random.choice(accept_languages),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
    }
    return headers

# 示例用法
headers = generate_random_headers()
def get_songs():
    cnn = pymysql.connect(host="localhost",
        user="root",
        password="1234567890asd",
        database="music_samp",
        charset="utf8mb4",)
    cursor = cnn.cursor()
    cursor.execute("SELECT `link`,`song_name` FROM `歌曲表`")
    song_list = cursor.fetchall()
    return song_list
def get_comments(song_link,song_name):
    offset = 0
    batch_size = 100
    url = f"https://music.163.com/api/v1/resource/comments/R_SO_4_{song_link}?limit={batch_size}&offset={offset}"
    headers = generate_random_headers()
    cnn = pymysql.connect(host="localhost",
        user="root",
        password="1234567890asd",
        database="music_samp",
        charset="utf8mb4",)
    cursor = cnn.cursor()
    while True:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = json.loads(response.text)
                total = data.get('total', 0)  # 获取评论总数
                comments = data.get('comments', [])
                print(f"当前请求返回评论数量: {len(comments)}，总评论数: {total}")
                if not comments:
                    break
                batch = []
                for comment in comments:
                    user = comment['user']['nickname']
                    content = comment['content']
                    liked = comment['likedCount']
                    batch.append((song_name,user, content, song_link, liked))

                if batch:
                    cursor.executemany(
                        "INSERT INTO `comment` (`song_name`,`user`, `content`, `song_link`, `liked`) VALUES (%s, %s, %s, %s,%s)",
                        batch
                    )
                    cnn.commit()
                offset += batch_size
                if offset >= total:  # 检查是否已获取所有评论
                    break
                url = f"https://music.163.com/api/v1/resource/comments/R_SO_4_{song_link}?limit={batch_size}&offset={offset}"
              # 增加请求间隔，避免触发限制
            else:
                print(f"请求失败，状态码：{response.status_code}")
                break
        except requests.exceptions.RequestException as e:
            print(f"请求异常：{e}")
            break
    print(f"歌曲 {song_name} 的评论获取完成！")

if __name__ == "__main__":
    songs = get_songs()

    for song in songs:
        song_link = song[0]
        song_name = song[1]
        get_comments(song_link,song_name)
        time.sleep(3)
