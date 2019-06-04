import json
import os
import shutil
import sqlite3
import time

import requests
from flask import Flask, render_template, request, make_response, jsonify, Response
from flask_cors import CORS
import spider
import musicapi
host = 'http://127.0.0.1:5000'
app = Flask(__name__)

CORS(app, resources=r'/*')
headers = {
        'Origin': 'https: // y.qq.com',
        'Referer': 'https://y.qq.com/portal/player.html',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
        'cookie': "pgv_pvi = 2947012608;RK = HkSsE + 5pVR;ptcz = f0ed9c02fb84919207e37a994303aceebc3e78791fdc987ecf03d06cab99f1c2;pgv_pvid = 2033232480;ts_uid = 9374732093;userAction = 1;luin = o1962348506;lskey = 00010000794c325f3e0b710c65fea26456651fd8e6cf5a36d637b16c277b21e34ad2c184e478a0785a67c44f;p_luin = o1962348506;p_lskey = 00040000fffa34ebaa81a056d764456a9f8436d4ebfad6386cdfefab88347255768b0e893f47de7cf2fd4465;ts_refer = ADTAGmyqq;yqq_stat = 0;pgv_info = ssid = s5115294120; pgv_si = s9392011264;ts_last = y.qq.com / portal / player.html;qqmusic_fromtag = 66;yplayer_open = 1;yq_playschange = 0;yq_playdata =;player_exist = 1;yq_index = 1"
    }


@app.route('/')
def hello_world():
    # results = spider.getSong("光明")
    # print(results)

    return "hello"


@app.route('/searchSongs')
def search_songs():

    # keyword = "画心"
    # url = "https://api.bzqll.com/music/tencent/search?key=579621905&s=" + keyword + "&limit=3&offset=0&type=song"
    # response = requests.get(url).json()
    type = request.args.get('type') # get args
    keyword = request.args.get('keyword')
    print(type,keyword)
    response = {}
    result =[]
    song_url = {}
    nums = '10'
    if type=='wangyiyun':
        post_url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token=' # search
        content = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": keyword, "type": "1", "offset": "0",
                   "total": "true", "limit": nums, "csrf_token": ""}
        response = musicapi.music163_interface(post_url,content)
        ids = [i['id'] for i in response['result']['songs']]


        song_url = musicapi.music163_geturl(ids) #get song's url


        for i in range(len(response['result']['songs'])):
            post_url = 'http://music.163.com/weapi/song/lyric?csrf_token='  # lrc url
            content = {"id": response['result']['songs'][i]['id'], "lv": -1, "tv": -1, "csrf_token": ""}
            lrc_data = musicapi.music163_interface(post_url, content)['lrc']['lyric']
            result.append({
                'id': response['result']['songs'][i]['id'],
                'name': response['result']['songs'][i]['name'],
                'artist': "、".join([i['name'] for i in response['result']['songs'][i]['ar']]),
                'url': song_url['data'][i]['url'],
                'cover': response['result']['songs'][i]['al']['picUrl'],
                'lrc': lrc_data,

            })
    elif type=='qq':
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=70389665041888426&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n='+nums+'&w='+keyword+'&g_tk=584747961&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0'
        res = requests.get(url)
        songInfoList = res.json()['data']['song']['list']
        print(songInfoList)

        songsurl = get_url_qq([i['file']['media_mid'] for i in songInfoList])
        for i in range(len(songInfoList)):
            lrc_url = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?-=MusicJsonCallback_lrc&pcachetime=1556535821223&songmid=" + songInfoList[i]['file']['media_mid'] + "&g_tk=584747961&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&nobase64=1"
            lrc_data = requests.get(lrc_url, headers=headers).json().get('lyric')
            result.append({
                'id':songInfoList[i]['file']['media_mid'],
                'name':songInfoList[i]['title'],
                'url':songsurl[i],
                'cover':"https://y.gtimg.cn/music/photo_new/T002R800x800M000" + songInfoList[i]['album']['mid'] + ".jpg",
                'artist':songInfoList[i]['singer'][0]['name'],
                'lrc':lrc_data,
            })
    elif type=='kugou':
        result = spider.get_song_kugou(keyword)
        print(result)

    return json.dumps(result,ensure_ascii=False)
    # results = spider.getSong("光明")


@app.route('/downloadSong', methods=['post', 'get'])
def download_song():

    data = json.loads(request.data)
    print(data)
    print(data['id'])
    # url = 'https://api.itooi.cn/music/tencent/url?id=000SMbk50otvvD&key=579621905'
    #
    file_name = data['name'] + '__' + data['artist']
    file_id = data['id']
    if not os.path.exists('./static/audios/' +data['username']):
        os.mkdir('./static/audios/' +data['username'])
    dir_name = './static/audios/' +data['username']+'/'+ file_id
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        res_url = requests.get(data['url'])
        print("res_url",res_url.status_code)
        with open(dir_name + '/' + file_name + '.mp3', 'wb') as f:
            f.write(res_url.content)
        res_cover = requests.get(data['cover'])
        print("res_cover", res_cover.status_code)
        with open(dir_name + '/' + file_name + '.jpg', 'wb') as f:
            f.write(res_cover.content)
        res_lrc = requests.get(data['lrc'])
        with open(dir_name + '/' + file_name + '.lrc', 'wb') as f:
            f.write(res_lrc.content)
        print("res_lrc", res_lrc.status_code)





    return json.dumps("SUCCESS")


"""
    get collections
    :return audiosData
    :type List 
"""


@app.route('/getCollections')
def get_collections():
    # base_dir = 'http://123.207.100.91:5000/static/audios'
    print(request.args)
    user = request.args.get('user')
    if user=="":
        return json.dumps([])

    base_dir = host+'/static/audios/'+user
    songs = [x for x in os.listdir('static/audios/'+user) if os.path.isdir('static/audios/' + user+'/'+x)]
    results = []
    for i in songs:
        file_name = [os.path.splitext(x)[0] for x in os.listdir('./static/audios/' +user+'/'+ i)][0].split('__')
        name = str(file_name[0]) + '__' + str(file_name[1])
        results.append({
            'id': i,
            'name': file_name[0],
            'artist': file_name[1],
            'url': base_dir + '/' + i + '/' + name + '.mp3',
            'cover': base_dir + '/' + i + '/' + name + '.jpg',
            'lrc': base_dir + '/' + i + '/' + name + '.lrc',

        })
    # print(results)
    return json.dumps(results,ensure_ascii=False)


@app.route('/removeCollection', methods=['post', 'get'])
def remove_collection():
    print(">>>>>>>>")

    print(json.loads(request.data))

    item = json.loads(request.data)
    base_dir = './static/audios/'+item.get('username')+'/'
    shutil.rmtree(base_dir + item.get('item'))
    return json.dumps("success")

"""
    :param songmid: mid list
"""
def get_url_qq(songmid):
    url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?_=' + str(round(time.time()) * 1000)
    filename = ["RS02" + i + ".mp3" for i in songmid]
    data = {"req_1": {"module": "vkey.GetVkeyServer", "method": "CgiGetVkey",
                      "param": {"guid": "2033232480", "songmid": songmid,
                                "uin": "0", "loginflag": 0, "platform": "23", "h5to": "speed",
                                "filename": filename}},
            "comm": {"g_tk": 5381, "uin": 0, "format": "json", "ct": 23, "cv": 0}}

    res = requests.post(url, data=json.dumps(data)).json()

    midurlinfo = res['req_1']['data']['midurlinfo']

    songurl = [
        "http://223.99.245.24/amobile.music.tc.qq.com/" + i['purl'].replace('RS02', 'C400').replace('.mp3', '.m4a') for
        i in midurlinfo]

    return songurl
@app.route('/getlrc')
def getlrc():
    type = request.args.get('type')
    songmid = request.args.get('songmid')
    lrc_data={}
    if type=='qq':
        lrc_url = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?-=MusicJsonCallback_lrc&pcachetime=1556535821223&songmid=" + songmid + "&g_tk=584747961&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&nobase64=1"
        lrc_data = requests.get(lrc_url, headers=headers).json()['lyric']
    elif type=='wangyiyun':
        post_url = 'http://music.163.com/weapi/song/lyric?csrf_token='  # lrc url
        content = {"id": songmid, "lv": -1, "tv": -1, "csrf_token": ""}
        lrc_data = musicapi.music163_interface(post_url, content)['lrc']['lyric']
    return json.dumps(lrc_data,ensure_ascii=False)


"""
    id: toplist type 4:流行  26:热歌 
"""


@app.route('/gettoplist')
def gettoplist():
    id = request.args.get('id')
    type = request.args.get('type')
    result = []
    period = time.strftime("%Y-%m-%d", time.localtime())
    period2 = time.strftime("%Y_%U", time.localtime())
    if type=='qq':
        headers = {
            'Referer': 'https://y.qq.com/n/yqq/toplist/'+id+'.html',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
        }
        if id=='26':
            print(id)
            url = "https://u.y.qq.com/cgi-bin/musicu.fcg?-=getUCGI20493628237831651&g_tk=584747961&loginUin=1962348506&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22detail%22%3A%7B%22module%22%3A%22musicToplist.ToplistInfoServer%22%2C%22method%22%3A%22GetDetail%22%2C%22param%22%3A%7B%22topId%22%3A26%2C%22offset%22%3A0%2C%22num%22%3A5%2C%22period%22%3A%22"+period2+"%22%7D%7D%2C%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%7D"
        elif id=='4':
            print(id)
            url = "https://u.y.qq.com/cgi-bin/musicu.fcg?-=getUCGI20500235302618308&g_tk=584747961&loginUin=1962348506&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22detail%22%3A%7B%22module%22%3A%22musicToplist.ToplistInfoServer%22%2C%22method%22%3A%22GetDetail%22%2C%22param%22%3A%7B%22topId%22%3A4%2C%22offset%22%3A0%2C%22num%22%3A5%2C%22period%22%3A%22"+period+"%22%7D%7D%2C%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%7D"
        elif id=='28':
            url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?-=getUCGI35663070925798834&g_tk=584747961&loginUin=1962348506&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22detail%22%3A%7B%22module%22%3A%22musicToplist.ToplistInfoServer%22%2C%22method%22%3A%22GetDetail%22%2C%22param%22%3A%7B%22topId%22%3A28%2C%22offset%22%3A0%2C%22num%22%3A5%2C%22period%22%3A%22'+period2+'%22%7D%7D%2C%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%7D'
        res = requests.get(url, headers=headers).json()
    # print(res)
        songInfoList = res['detail']['data']['songInfoList']

        songmid = [i['file']['media_mid'] for i in songInfoList] # used to get songurl
        filename = ["RS02"+i+".mp3" for i in songmid] # used to get songurl

        # print(songmid)

        url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?_=' + str(round(time.time()) * 1000)

        data = {"req_1": {"module": "vkey.GetVkeyServer", "method": "CgiGetVkey",
                          "param": {"guid": "2033232480", "songmid": songmid,
                                    "uin": "0", "loginflag": 0, "platform": "23", "h5to": "speed",
                                    "filename": filename}},
                "comm": {"g_tk": 5381, "uin": 0, "format": "json", "ct": 23, "cv": 0}}

        res = requests.post(url, data=json.dumps(data)).json()

        midurlinfo = res['req_1']['data']['midurlinfo']

        songurl = ["http://223.99.245.24/amobile.music.tc.qq.com/"+i['purl'].replace('RS02','C400').replace('.mp3','.m4a') for i in midurlinfo]
        # print(songInfoList)
        for i in range(len(songInfoList)):
            result.append({
                'id':songInfoList[i]['file']['media_mid'],
                'name':songInfoList[i]['name'],
                'url':songurl[i],
                'cover':"https://y.gtimg.cn/music/photo_new/T002R800x800M000" + songInfoList[i]['album']['mid'] + ".jpg",
                'artist':songInfoList[i]['singer'][0]['name'],
                'lrc':host+"/getlrc?songmid="+songInfoList[i]['file']['media_mid'],
            })
    elif type=='wangyiyun':
        post_url = 'http://music.163.com/weapi/v3/playlist/detail?csrf_token='  # toplist
        content = {
            "id": id,
            "offset": 0,
            "total": True,
            "limit": 10,
            "n": 10,
            "csrf_token": ""
        }
        playlist = musicapi.music163_interface(post_url, content)
        playlist = playlist['playlist']['tracks']
        ids = [i['id'] for i in playlist]
        song_url = musicapi.music163_geturl(ids)

        for i in range(len(playlist)):
            result.append({
                'id': playlist[i]['id'],
                'name': playlist[i]['name'],
                'artist': "、".join([i['name'] for i in playlist[i]['ar']]),
                'url': song_url['data'][i]['url'],
                'cover': playlist[i]['al']['picUrl'],
                'lrc': host + '/getlrc?type=wangyiyun&songmid=' + str(playlist[i]['id']),
            })


        print(result)

    return json.dumps(result,ensure_ascii=False)

@app.route('/login',methods=['post','get'])
def login():
    print(request.form)
    conn = sqlite3.connect('user.db')
    c = conn.cursor()

    cursor = c.execute('select * from user where name=?', (request.form.get('name'),))
    if cursor.fetchone():
        return request.form.get('name')

    c.close()
    conn.close()
    return "error"

if __name__ == '__main__':
    app.run(host="0.0.0.0",port="5000")
