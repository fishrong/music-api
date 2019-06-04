from Crypto.Cipher import AES
import base64
import json
import requests

# 常量
headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0',
    'Referer':
    'https://music.163.com/',
    'Content-Type':
    'application/x-www-form-urlencoded',
}
# post_url = 'https://music.163.com/weapi/song/enhance/player/url'
# post_url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token='
# content = {"ids": "", "br": 128000, "csrf_token": ""}
# content = {"hlpretag":"<span class=\"s-fc7\">","hlposttag":"</span>","s":"爱","type":"1","offset":"0","total":"true","limit":"30","csrf_token":""}
key1 = b'0CoJUm6Qyw8W8jud'
key2 = b'ryPnuAVT5RtiIWNi'
encSecKey = 'a71973af53caae445b554150da52e75ba5687609d28013aacea03e9ef07169560f156ca76be9ac8df7bb204e05b864756aa3dd2274a65d5be964f118f6d075006695059e10cdcc806306e9a5f2f36f5bf0379f511cd13a600a6cc7031c814583863ea84d3373dea69f74354cd2dc3af61d58eeb43b1de06f588ef361ebc1eed6'

# 加密
pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
encrypt_token = lambda key, content: AES.new(key=key, mode=AES.MODE_CBC, IV=b'0102030405060708').encrypt(pad(content).encode())


# 接口
def music163_interface(post_url,content):
    str_content = json.dumps(content)
    tmp = base64.b64encode(encrypt_token(key1, str_content)).decode()
    params = base64.b64encode(encrypt_token(key2, tmp)).decode()
    post_data = {
        'params': params,
        'encSecKey': encSecKey,
    }
    resp = requests.post(url=post_url, headers=headers, data=post_data)
    js = json.loads(resp.content)
    return js

def music163_geturl(ids):
    post_url = 'https://music.163.com/weapi/song/enhance/player/url'  # song url
    content = {"ids": ids, "br": 320000, "csrf_token": ""}
    song_url = music163_interface(post_url, content)
    print(">>>songutl",song_url)
    return song_url

if __name__ == '__main__':
    # post_url = 'http://music.163.com/weapi/cloudsearch/get/web?csrf_token=' # search
    # content = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": "爱", "type": "1", "offset": "0",
    #            "total": "true", "limit": "30", "csrf_token": ""}
    post_url = 'http://music.163.com/weapi/v3/playlist/detail?csrf_token='#toplist
    content = {
                "id": 3778678,
                "offset": 0,
                "total": True,
                "limit": 10,
                "n": 10,
                "csrf_token": ""
            }
    song_url = music163_interface(post_url,content)
    print(song_url)