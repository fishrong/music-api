import json

import requests
import time

id = '4'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https: // y.qq.com',
    'Referer': 'https://y.qq.com/n/m/detail/toplist/index.html?ADTAG=myqq&from=myqq&channel=10007100&id=26',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    # 'cookie': "pgv_pvi = 2947012608;RK = HkSsE + 5pVR;ptcz = f0ed9c02fb84919207e37a994303aceebc3e78791fdc987ecf03d06cab99f1c2;pgv_pvid = 2033232480;ts_uid = 9374732093;userAction = 1;luin = o1962348506;lskey = 00010000794c325f3e0b710c65fea26456651fd8e6cf5a36d637b16c277b21e34ad2c184e478a0785a67c44f;p_luin = o1962348506;p_lskey = 00040000fffa34ebaa81a056d764456a9f8436d4ebfad6386cdfefab88347255768b0e893f47de7cf2fd4465;ts_refer = ADTAGmyqq;yqq_stat = 0;pgv_info = ssid = s5115294120; pgv_si = s9392011264;ts_last = y.qq.com / portal / player.html;qqmusic_fromtag = 66;yplayer_open = 1;yq_playschange = 0;yq_playdata =;player_exist = 1;yq_index = 1"
}
url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?_=' + str(round(time.time()) * 1000)

data = {"req_1": {"module": "vkey.GetVkeyServer", "method": "CgiGetVkey",
                  "param": {"guid": "2033232480", "songmid": ["004dgN9x2ZdeW8", "001J5QJL1pRQYB"],
                            "uin": "0", "loginflag": 0, "platform": "23", "h5to": "speed",
                            "filename": ["RS02004dgN9x2ZdeW8.mp3", "RS02001J5QJL1pRQYB.mp3"]}},
        "comm": {"g_tk": 5381, "uin": 0, "format": "json", "ct": 23, "cv": 0}}

res = requests.post(url,  data=json.dumps(data)).json()
print(res)

print(round(time.time()) * 1000)
