import requests


def get_cloudmusic_top_songs():
    # 网易云官方API接口（热歌榜ID：3778678）
    api_url = "https://music.163.com/api/playlist/detail"

    # 必要的请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://music.163.com/'
    }

    params = {
        'id': '3778678',  # 榜单ID
        'updateTime': '-1'
    }

    try:
        response = requests.get(api_url, headers=headers, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()
        songs = data['result']['tracks']

        # 提取歌曲名称
        return [song['name'] for song in songs]

    except Exception as e:
        print(f"获取数据失败: {str(e)}")
        return []


if __name__ == "__main__":
    song_list = get_cloudmusic_top_songs()
    for idx, song in enumerate(song_list, 1):
        print(f"{idx}. {song}")