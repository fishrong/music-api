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
    'Origin': 'https://y.qq.com',
    'Referer': 'https://y.qq.com/portal/player.html',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Mobile Safari/537.36'
}


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


def get_song_qq(keyword):
    keyword = keyword
    info_url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?g_tk=5381&p=1&n=5&w=" + keyword + "&format=json&loginUin=0&hostUin=0&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&remoteplace=txt.yqq.song&t=0&aggr=1&cr=1&catZhida=1&flag_qc=0"
    info_req = session.get(info_url, headers=headers).json()
    # print(info_req)
    print(info_req['data']['song']['list'][2])
    songmid = info_req['data']['song']['list'][2]['songmid']
    v_key_url = "https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey18590248262541031&g_tk=654540112&loginUin=1490860381&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22req%22%3A%7B%22module%22%3A%22CDN.SrfCdnDispatchServer%22%2C%22method%22%3A%22GetCdnDispatch%22%2C%22param%22%3A%7B%22guid%22%3A%222033232480%22%2C%22calltype%22%3A0%2C%22userip%22%3A%22%22%7D%7D%2C%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%222033232480%22%2C%22songmid%22%3A%5B%22"+songmid+"%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%221490860381%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A1490860381%2C%22format%22%3A%22json%22%2C%22ct%22%3A24%2C%22cv%22%3A0%7D%7D"
    v_key_req = session.get(v_key_url, headers=headers).json()
    print(v_key_req)
    v_key = v_key_req['req_0']['data']['midurlinfo'][0]['purl']
    print("key",v_key)

    # filename = v_key_req['data']['items'][2]['filename']
    # print(v_key)

               #http://isure.stream.qqmusic.qq.com/C400000OTLDc2Z35Wr.m4a?guid=2033232480&vkey=79A1A4066EEC3001FF185733147D0101A158E03C07165334E0E38674CD22AB071A4549489EB7B666269349F5C548DFB80599D9A99CCF4515&uin=6493&fromtag=66
    song_url = "http://isure.stream.qqmusic.qq.com/"+v_key
    print(song_url)
    print(v_key_req['req_0']['data']['midurlinfo'])
    # print("http://isure.stream.qqmusic.qq.com/C400000OTLDc2Z35Wr.m4a?guid=2033232480&vkey=79A1A4066EEC3001FF185733147D0101A158E03C07165334E0E38674CD22AB071A4549489EB7B666269349F5C548DFB80599D9A99CCF4515&uin=6493&fromtag=66")
    # song_url_req = requests.get(song_url, headers=headers)
    # print(">>>>>")
    # print(song_url_req.text)  M500000Cubqa3VgCrk  RS02000Cubqa3VgCrk.mp3


if __name__ == '__main__':
    # print(getSong("浪子回头"))
    get_song_qq("画心")
    # # rankSong()
    # print(int(time.time() * 1000))

    # #playSongs()
