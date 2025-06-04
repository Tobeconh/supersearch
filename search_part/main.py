import sys
from concurrent.futures import ThreadPoolExecutor
from crawler.ncm_crawler import get_songs_from_ncm_playlist
from manageData.manageData import manageData


def fetch_and_store(playlist_id,table_name):

    
    ncm_songlist = get_songs_from_ncm_playlist(playlist_id)
    formatted_data = [
        (item["rank"], item["name"], item["time"], item["singer"], item["link"])
        for item in ncm_songlist
    ]
    key_list = ["rank", "name", "time", "singer", "link"]
    manageData(formatted_data, table_name, key_list)
def main():
    playlist_ids = [
        "71384707",
        "1978921795",
        "991319590",
        "60198",
        '180106'
    ]
    tables_name=["古典榜",
                 "电音榜",
                 "说唱榜",
                 "bilibili热门榜",
                 'UK排行榜'
                 ]
    with ThreadPoolExecutor(max_workers=5) as executor:
        for playlist_id in playlist_ids:
            table_name = tables_name[playlist_ids.index(playlist_id)]
            executor.submit(fetch_and_store, playlist_id, table_name)
if __name__ == "__main__":
    main()
