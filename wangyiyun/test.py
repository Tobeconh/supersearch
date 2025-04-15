from time import sleep

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import json
from search_part import seach
testdriver = seach.seach()
#加载失败报错，否则继续执行程序
try:
    testdriver.get("https://y.qq.com/n/ryqq/toplist/26")
except Exception as e:
    print("加载失败:", e)
    testdriver.quit()
    exit(1)
#等待页面加载完成
WebDriverWait(testdriver,15).until(
    lambda d:d.execute_script("return document.readyState;")=="complete"
)

sleep(5)
print(testdriver.page_source)
soup = BeautifulSoup(testdriver.page_source, "html")
all_songs_data = []
songlist =soup.find('ul',class_="songlist__list").find_all('li')
print('正在爬取数据...')
print(songlist)
for song in songlist:
    print(song)
    rank = song.select_one('.songlist__item > .songlist__number').get_text(strip=True)
    name =song.find(class_="songlist__songname_txt").get_text(strip=True)
    time = song.find(class_='songlist__time').get_text(strip=True)
    singer = song.find(class_='songlist__artist').get_text(strip=True)
    data = {'rank':rank,'name':name,'time':time,'singer':singer}
    all_songs_data.append(data)
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(all_songs_data, f, ensure_ascii=False, indent=4)
testdriver.quit()




