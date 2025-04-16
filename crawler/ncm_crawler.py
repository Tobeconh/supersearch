"""网易云音乐爬虫"""

from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .crawler_factory import create_normal_crawler


def extract_song_data_from_element(element):
    """从element中提取歌曲信息"""
    rank = element.select_one(".num").get_text(strip=True)
    song_to_link = element.select_one(".ttc a[href]")["href"].replace("/song?id=", "")

    song_link = element.select_one(".ttc a b")

    name = (
        song_link["title"].replace("&nbsp;", " ").replace(" ", " ")
        if song_link and song_link.has_attr("title")
        else ""
    )

    time = element.select_one(".u-dur").get_text(strip=True)
    singer_element = element.select_one(".text[title]")
    singer = (
        singer_element["title"].replace("&nbsp;", " ").replace(" ", " ")
        if singer_element and singer_element.has_attr("title")
        else ""
    )

    return {"rank": rank, "name": name, "time": time, "singer": singer, "link": song_to_link}


def get_songs_from_ncm_playlist(playlist_id: str):
    """通过网易云歌单id获取曲目"""
    crawler = create_normal_crawler()
    # 加载失败报错，否则继续执行程序
    try:
        crawler.get(f"https://music.163.com/#/discover/toplist?id={playlist_id}")
    except TimeoutError as e:
        print("加载失败:", e)
        crawler.quit()
        exit(1)
    print("加载中")
    # 等待页面加载完成
    crawler.switch_to.frame("contentFrame")
    WebDriverWait(crawler, 15).until(
        EC.presence_of_element_located((By.ID, "song-list-pre-cache"))
    )

    sleep(5)
    # print(crawler.page_source)
    soup = BeautifulSoup(crawler.page_source, "html")
    song_elements = soup.find(id="song-list-pre-cache").find("tbody").find_all("tr")
    print("正在爬取数据...")
    # print(song_elements)
    crawler.quit()

    return [extract_song_data_from_element(song) for song in song_elements]
