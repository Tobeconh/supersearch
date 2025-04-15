"""qq音乐爬虫"""

from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait

from .crawler_factory import create_normal_crawler


def extract_song_data_from_element(element):
    """从element中提取歌曲信息"""
    rank = element.select_one(".songlist__item > .songlist__number").get_text(
        strip=True
    )
    name = element.find(class_="songlist__songname_txt").get_text(strip=True)
    time = element.find(class_="songlist__time").get_text(strip=True)
    singer = element.find(class_="songlist__artist").get_text(strip=True)
    return {"rank": rank, "name": name, "time": time, "singer": singer}


def get_songs_from_qq_playlist(playlist_id: str):
    """通过qq歌单id获取曲目"""
    crawler = create_normal_crawler()
    # 加载失败报错，否则继续执行程序
    try:
        crawler.get(f"https://y.qq.com/n/ryqq/toplist/{playlist_id}")
    except TimeoutError as e:
        print("加载失败:", e)
        crawler.quit()
        exit(1)
    print("加载中")
    # 等待页面加载完成
    WebDriverWait(crawler, 15).until(
        lambda d: d.execute_script("return document.readyState;") == "complete"
    )

    sleep(5)
    # print(crawler.page_source)
    soup = BeautifulSoup(crawler.page_source, "html")
    song_elements = soup.find("ul", class_="songlist__list").find_all("li")
    print("正在爬取数据...")
    crawler.quit()

    return [extract_song_data_from_element(song) for song in song_elements]