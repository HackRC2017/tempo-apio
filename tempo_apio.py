import functools
import html
import os
import re

import pymongo
from bson.json_util import dumps
from flask import Flask
from flask import jsonify
from flask import request
from flask import Response


__version__ = '0.1.0'
app = Flask(__name__)

FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)
MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
MONGODB_PORT = os.environ.get('MONGODB_PORT', 27017)
MONGODB_DB = os.environ.get('MONGODB_DB', 'tempo')

mongo_client = pymongo.MongoClient(MONGODB_HOST, MONGODB_PORT)
db = mongo_client[MONGODB_DB]
articles = db.articles


@functools.lru_cache(maxsize=64)
def get_anchor_pattern(anchor):
    return re.compile(r'<!--.*?' + anchor + '\\"\}-->')

def fetch_articles(size, max_readtime=0, themes=None):
    query_filter = {}
    if max_readtime > 0:
        query_filter['readTime.total.minutes'] = {'$lte': max_readtime}
    if themes:
        query_filter['themeTag.id'] = {'$in': themes}

    return articles.find(query_filter)\
                   .sort('publishedFirstTimeAt', pymongo.DESCENDING)\
                   .limit(size)


def transform_body(body):
    for attachment in body.get('attachments', []):

        try:
            # Extract info
            anchor = attachment['anchor']['fragmentId']
            legend = html.escape(attachment['conceptualImage']['legend'])
            alt_text = html.escape(attachment['conceptualImage']['alt'])
            href = attachment['conceptualImage']['concreteImages'][0]['mediaLink']['href']

            # Substitute comments
            image_element = f'<img src="{href}" alt="{alt_text}"/>'
            caption = f'<figcaption>{legend}</figcaption>'
            pattern = get_anchor_pattern(anchor)
            body['html'] = re.sub(pattern, image_element + caption, body['html'])
        except KeyError:
            pass

    return body


@app.route('/version')
def get_version():
    return __version__


@app.route('/articles')
def get_articles():
    max_readtime = request.args.get('max_readtime', default=10, type=int)
    size = request.args.get('size', default=10, type=int)
    themes = request.args.get('themes')
    if themes:
        themes = themes.split(',')

    articles = list(fetch_articles(size, max_readtime, themes))
    for article in articles:
        article["body"] = transform_body(article["body"])
    payload = dumps({'articles': articles})
    return Response(response=payload,
                    mimetype="application/json")


@app.route('/caneton_stats')
def get_caneton_stats():
    s = db.stats.find({}, {'_id': False}).sort('datetime', pymongo.DESCENDING)
    return jsonify(list(s))


if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=5001)
