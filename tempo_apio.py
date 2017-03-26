import os

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


def fetch_articles(size, max_readtime):
    query_filter = {
        'readTime.total.minutes': {
            '$lte': max_readtime
        }
    }
    return articles.find(query_filter)\
                   .limit(size)

@app.route('/version')
def get_version():
    return __version__


@app.route('/articles')
def get_articles():
    max_readtime = request.args.get('max_readtime', default=10, type=int)
    size = request.args.get('size', default=10, type=int)
    payload = dumps({'articles': list(fetch_articles(size, max_readtime))})
    return Response(response=payload,
                    mimetype="application/json")


@app.route('/caneton_stats')
def get_caneton_stats():
    s = db.stats.find({}, {'_id': False}).sort('datetime', pymongo.DESCENDING)
    return jsonify(list(s))


if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG, host='0.0.0.0', port=5001)
