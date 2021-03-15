from flask import Flask, jsonify
import backend

app = Flask(__name__)


@app.route('/api/events')
def events():
    return jsonify(backend.getEvents())

if __name__ == '__main__':
    app.run()