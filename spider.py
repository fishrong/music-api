import gzip
import json
import time
import urllib3
from datetime import date
from random import random
from urllib.parse import quote
import requests

session = requests.Session()
# k = PyKeyboard()
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'kg_mid=8422b7a2bfaa1dec5cc91ce4750a174c; kg_dfid=1sC9iB4RPnfz0FXqSP4F7KH2; Hm_lvt_aedee6983d4cfc62f509129360d6bb3d=1555555239,1555846420,1555846430',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}


# 获取单首歌链接
def get_song_kugou(keyword):
    songs = []
    keyword = keyword
    info_url = "http://songsearch.kugou.com/song_search_v2?callback=jQuery19107655316341116605_1497970603262&keyword=" + keyword + "&page=1&pagesize=5&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0"
    info_req = session.get(info_url, headers=headers).text

    info_text = json.loads(info_req[41:-2])
    # print(info_text)
    songlist = info_text['data']['lists']
    info_song = info_text['data']['lists'][0]['FileName']
    # print("正在播放：" + info_song)
    FileHash = info_text['data']['lists'][0]['FileHash']
    AlbumID = info_text['data']['lists'][0]['AlbumID']
    # print(len(info_text['data']['lists']))
    # print("songlist",songlist)
    for i in range(len(songlist)):
        FileHash = songlist[i]['FileHash']
        AlbumID = songlist[i]['AlbumID']
        mp3_url = "http://www.kugou.com/yy/index.php?r=play/getdata&hash=" + FileHash + "&album_id=" + AlbumID + "&_=1497972864535"
        mp3_req = session.get(mp3_url, headers=headers).text
        text = json.loads(mp3_req)
        print(text)
        songs.append({
            "id": info_text['data']['lists'][i]['Audioid'],
            "name": text['data']['song_name'],
            "artist": text['data']['author_name'],
            "url": text['data']['play_url'],
            "cover": text['data']['img'],
            'lrc':text['data']['lyrics']
        })

    # print("songs",songs)

    return songs
def get_lrc_kugou():

    pass

if __name__ == '__main__':
    # print(getSong("浪子回头"))
    # get_song_qq("画心")
    # # rankSong()
    # print(int(time.time() * 1000))

    get_song_kugou("love you like")
