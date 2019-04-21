import json
import os

import requests
from flask import Flask, render_template, request, make_response
from flask.json import jsonify
from flask_cors import CORS

import spider

app = Flask(__name__)

CORS(app, resources=r'/*')


@app.route('/')
def hello_world():
    # results = spider.getSong("光明")
    # print(results)

    return "hello"


@app.route('/searchSongs')
def search_songs():
    keyword = "画心"
    url = "https://api.bzqll.com/music/tencent/search?key=579621905&s=" + keyword + "&limit=3&offset=0&type=song"
    response = requests.get(url).json()
    return response
    # results = spider.getSong("光明")


@app.route('/downloadSong', methods=['post', 'get'])
def download_song():
    print(request.form)
    print(request.form['list[url]'])

    # url = 'https://api.itooi.cn/music/tencent/url?id=000SMbk50otvvD&key=579621905'

    file_name = request.form['list[name]'] + '__' + request.form['list[artist]']
    file_id = request.form['list[id]']
    dir_name = './static/audios/' +file_id
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        res_url = requests.get(request.form['list[url]'])
        res_cover = requests.get(request.form['list[cover]'])
        res_lrc = requests.get(request.form['list[lrc]'])
        print(res_url.status_code)
        with open(dir_name + '/' +file_name+'.mp3', 'wb') as f:
            f.write(res_url.content)

        with open(dir_name + '/' +file_name+ '.jpg', 'wb') as f:
            f.write(res_cover.content)

        with open(dir_name + '/' +file_name+ '.lrc', 'wb') as f:
            f.write(res_lrc.content)
    return "SUCCESS"


@app.route('/getCollections')
def get_collections():
    base_dir = 'http://123.207.100.91:5000/static/audios'
    songs = [x for x in os.listdir('static/audios') if os.path.isdir('static/audios/'+x)]
    results = []
    for i in songs:
        file_name = [os.path.splitext(x)[0] for x in os.listdir('./static/audios/'+i)][0].split('__')
        name = str(file_name[0])+'__'+str(file_name[1])
        results.append({
            'id': i,
            'name': file_name[0],
            'singer':file_name[1],
            'url': base_dir+'/'+i+'/'+name+'.mp3',
            'pic': base_dir+'/'+i+'/'+name+'.jpg',
            'lrc': base_dir+'/'+i+'/'+name+'.lrc',

        })
    print(results)
    return json.dumps(results)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
