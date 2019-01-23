import os
import importlib
from flask import Flask, current_app, send_file
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder="../dist/static")

from .config import Config

socketio = SocketIO(app)


@app.route("/")
def index_client():
    dist_dir = current_app.config["DIST_DIR"]
    entry = os.path.join(dist_dir, "index.html")
    return send_file(entry)


@socketio.on("listen_logs")
def client_msg(msg):
    emit("server_response", {"data": msg["data"]})
