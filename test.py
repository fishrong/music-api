import os

base_dir = 'http://127.0.0.1/static/audios'
songs = [x for x in os.listdir('static/audios') if os.path.isdir(x)]
results = []
for i in songs:
    results.append({
        'name': i.split('-')[1],
        'artist': i.split('-')[0],
        'url': base_dir + '/' + i + '/' + i + '.mp3',
        'cover': base_dir + '/' + i + '/' + i + '.jpg',
        'lrc': base_dir + '/' + i + '/' + i + '.lrc',
    })
print(results)
