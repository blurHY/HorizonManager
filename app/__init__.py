import os
from os.path import join
from flask import Flask, current_app, send_file
from flask_socketio import SocketIO, emit
from .watcher import watchLogs
from .config import Config
from .flaskConfig import flaskConfig

from .process import *

app = Flask(__name__, static_folder="../dist/static")

sio = SocketIO(app)

conf = Config()

zeronetProc = None
spiderProc = None


@app.route("/")
def index_client():
    dist_dir = current_app.config["DIST_DIR"]
    entry = os.path.join(dist_dir, "index.html")
    return send_file(entry)


@sio.on("connect")
def connected():
    print("Connected")
    updateProcessStatus()


@sio.on("subscribeLogs")
def subscribeLogs():
    print("Logs subscribed")
    watchLogs()


@sio.on("processControl")
@passwordRequired
def processControl(process, action):
    # if action not in [s]
    if process == "zeronet":
        if action == "start":
            startZeroNet()
        elif action == "stop":
            zeronetProc.terminate()
        elif action == "kill":
            zeronetProc.kill()
    elif process == "spider":
        if action == "start":
            startSpider()
        elif action == "stop":
            spiderProc.terminate()
        elif action == "kill":
            spiderProc.kill()
    else:
        showMessage("warning", f"Unknown process: {process}")
    updateProcessStatus()


@sio.on("getStats")
def getStats():
    # TODO: Stats
    emit("updateStats")


def checkPassword(password):
    correctPw = os.getenv("HorizonPassword")
    if correctPw is None:
        showMessage("warning", "Please set a password")
        return True
    if password == correctPw:
        return True
    else:
        wrongPassword()
        return False


def passwordRequired(func):
    def wrapper(password):
        if checkPassword(password):
            return func()

    return wrapper


def updateProcessStatus():
    fun = lambda bo: "Running" if bo else "Down"
    setStatus("ZeroNet: {0},Spider: {1}".format(
        fun(isRunning(zeronetProc)), fun(isRunning(spiderProc))))


def setStatus(msg):
    print("Status: " + msg)
    emit("setStatus", msg)


def showMessage(type, msg):
    emit("showMessage", type, msg)


def wrongPassword():
    showMessage("warning", "Incorrect password")
