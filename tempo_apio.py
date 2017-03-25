from flask import Flask, jsonify, request


__version__ = '0.1.0'
app = Flask(__name__)


@app.route('/version')
def version():
    return __version__


@app.route('/articles')
def articles():
    time = request.args.get('time', default=10, type=int)
    number = request.args.get('number', default=10, type=int)
    return jsonify([])
