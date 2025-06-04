import jieba
import pymysql
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
# 获取系统字体路径
import json
font_path = "/System/Library/Fonts/Supplemental/Songti.ttc"  # macOS 示例

conn = pymysql.connect(host='localhost',
                           user='root',
                           password='1234567890asd',
                           database='music_samp',
                           charset='utf8mb4')
cursor = conn.cursor()
# 读取数据
cursor.execute("SELECT `content` FROM `comment` WHERE `song_link`= 150432")
comments = cursor.fetchall()
# 关闭游标和连接
cursor.close()
conn.close()
# 将获得数据变为字符串
comments_str = ''.join([comment[0] for comment in comments])
from zhipuai import ZhipuAI

client = ZhipuAI(api_key='c7d8837d7596477e9a457cf38f6d0463.8uGIVHQ4SiCGNhfS')#api key
response = client.chat.completions.create(
        model='glm-4-air-250414',
         messages=[
            {'role': 'user', 'content': '对于之后的评论数据进行主要关键词提取'},
             {'role': 'user', 'content': comments_str},
        ],
        response_format={
            'type':'json_object',
        }
)
#保存关键词
with open('keywords.json', 'w', encoding='utf-8') as f:
    json.dump(response.choices[0].message.content, f, ensure_ascii=False, indent=4)
print(response.choices[0].message.content)
print(response.choices[0].resp)
