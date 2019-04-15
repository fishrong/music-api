import json

import requests

session = requests.Session()
# k = PyKeyboard()
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
           "Accept": "text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}


# 获取单首歌链接
def getSong(keyword):
    songs = []
    keyword = keyword
    info_url = "http://songsearch.kugou.com/song_search_v2?callback=jQuery19107655316341116605_1497970603262&keyword=" + keyword + "&page=1&pagesize=5&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0"
    info_req = session.get(info_url, headers=headers).text

    info_text = json.loads(info_req[41:-2])
    # print(info_text)
    info_song = info_text['data']['lists'][0]['FileName']
    # print("正在播放：" + info_song)
    FileHash = info_text['data']['lists'][0]['FileHash']
    AlbumID = info_text['data']['lists'][0]['AlbumID']
    # print(len(info_text['data']['lists']))
    for i in range(5):
        FileHash = info_text['data']['lists'][i]['FileHash']
        AlbumID = info_text['data']['lists'][i]['AlbumID']
        mp3_url = "http://www.kugou.com/yy/index.php?r=play/getdata&hash=" + FileHash + "&album_id=" + AlbumID + "&_=1497972864535"
        mp3_req = session.get(mp3_url, headers=headers).text
        text = json.loads(mp3_req)
        songs.append({
            "id": info_text['data']['lists'][i]['Audioid'],
            "title": info_text['data']['lists'][i]['SongName'],
            "singer": info_text['data']['lists'][i]['SingerName'],
            "songUrl": text['data']['play_url'],
            "imageUrl": text['data']['img'],
        })
    # print(AlbumID)
    # http://www.kugou.com/yy/index.php?r=play/getdata&hash=3C3D93A5615FB42486CAB22024945264&album_id=1645030&_=1497972864535
    # mp3_url = "http://www.kugou.com/yy/index.php?r=play/getdata&hash=" + FileHash + "&album_id=" + AlbumID + "&_=1497972864535"
    # mp3_req = session.get(mp3_url, headers=headers).text
    # text = json.loads(mp3_req)
    # list_s = text['result']['songs']
    # print(text['data'])
    # print(text['data']['authors']['audio_id'])
    # play_url = text['data']['play_url']

    return songs


if __name__ == '__main__':
    print(getSong("汪峰的光明"))
    # rankSong()
    # #playSongs()
