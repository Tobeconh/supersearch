import json
from crawler.qq_crawler import get_songs_from_qq_playlist
from crawler.ncm_crawler import get_songs_from_ncm_playlist


def main():
    # qq_songlist = get_songs_from_qq_playlist("26")
    # with open("qq_data.json", "w", encoding="utf-8") as f:
    #     json.dump(qq_songlist, f, ensure_ascii=False, indent=4)
    
    ncm_songlist = get_songs_from_ncm_playlist("3779629")
    with open("ncm_data.json", "w", encoding="utf-8") as f:
        json.dump(ncm_songlist, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
