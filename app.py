import json

from flask import Flask, render_template, request
import spider
app = Flask(__name__)


@app.route('/')
def hello_world():
    results = spider.getSong("光明")
    print(results)
    return render_template('index.html',results = results)


@app.route('/searchSongs')
def search_songs():
    print(request.args.get("keywords"))
    keywords = request.args.get("keywords")
    results = spider.getSong(keywords)
    return json.dumps(results)
    # results = spider.getSong("光明")



if __name__ == '__main__':
    app.run()
