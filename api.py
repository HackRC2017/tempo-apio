from flask import Flask, jsonify, request

import rad_can
rad_can.load_theme_lineups()


__version__ = '0.1.0'
app = Flask(__name__)


@app.route('/version')
def version():
    return __version__


@app.route('/articles')
def articles():
    time = request.args.get('time', default=10, type=int)
    number = request.args.get('number', default=10, type=int)
    return jsonify(rad_can.get_articles(number))
