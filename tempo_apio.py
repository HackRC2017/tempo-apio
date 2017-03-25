from flask import Flask, jsonify, request

import rad_can


__version__ = '0.1.0'
app = Flask(__name__)


@app.before_first_request
def _run_on_start():
    rad_can.load_articles(number=100, from_file=True)


@app.route('/version')
def version():
    return __version__


@app.route('/articles')
def articles():
    time = request.args.get('time', default=10, type=int)
    number = request.args.get('number', default=10, type=int)
    return jsonify(rad_can.get_articles(number))
