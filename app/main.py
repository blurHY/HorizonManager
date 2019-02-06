import datetime
import os
import shutil
import threading
import time
from os.path import join

import flask
import flask_login
import psutil
from flask import Flask, current_app, send_file
from flask_socketio import emit, join_room, leave_room
from humanize import naturalsize

from . import logs, process

from . import app, login_manager, sio, users
from .flaskConfig import flaskConfig


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    if username not in users:
        return

    user = User()
    user.id = username
    user.is_authenticated = request.form['password'] == users[username][
        'password']

    return user


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        flask.abort(400)
    print(flask.request.form)
    username = flask.request.form['username']
    try:
        if flask.request.form['password'] == users[username]['password']:
            user = User()
            user.id = username
            remember = flask.request.form.get("remember")
            flask_login.login_user(
                user,
                remember=True,
                duration=datetime.timedelta(
                    days=7) if remember else datetime.timedelta(hours=1))
            return flask.redirect("/")
        else:
            return "Invalid passworrd or username"
    except KeyError:
        return "User not found"

    return "Bad request"


@app.route('/api/logout', methods=['GET', 'POST'])
def logout():
    flask_login.logout_user()
    return 'Logged out'


def apiLoginCheck(func):
    def wrapper(*args, **kwargs):
        if flask_login.current_user.is_authenticated:
            func(*args, *kwargs)
        else:
            print("Unauthorized: " + str(func))
            showMessage("warning", "Unauthorized operation")
            setStatus("Unauthorized")
            sio.emit("redirect", "/login")

    return wrapper


@app.route('/')
@app.route('/<path:path>')
def index_client(*args, **kwargs):
    print(flask.request.path)
    if not flask_login.current_user.is_authenticated and flask.request.path != "/login":
        return flask.redirect("/login")
    dist_dir = current_app.config["DIST_DIR"]
    entry = os.path.join(dist_dir, "index.html")
    return send_file(entry)


@sio.on("connect")
@apiLoginCheck
def connected():
    print("Connected " + flask.request.sid)
    updateProcessStatus()
    setStatus("Ready")
    join_room("admins")
    updateAllRightNow()


@sio.on("disconnect")
@apiLoginCheck
def disconnected():
    print("Disconnected " + flask.request.sid)
    leave_room("admins")


@sio.on("processControl")
@apiLoginCheck
def processControl(proc, action):
    setStatus(f"{action.capitalize()}ing {proc}")
    try:
        if proc == "zeronet":
            if action == "start":
                process.startZeroNet()
            elif action == "stop":
                process.zeronetProc.terminate()
            elif action == "kill":
                process.zeronetProc.kill()
        elif proc == "spider":
            if action == "start":
                process.startSpider()
            elif action == "stop":
                process.spiderProc.terminate()
            elif action == "kill":
                process.spiderProc.kill()
        else:
            showMessage("warning", f"Unknown process: {proc}")
    except Exception as e:
        showMessage("error", f"An error occurred while {action}ing {proc}")
        setStatus("Ready")
        print(e)
    else:
        setStatus("Done")
    updateProcessStatus()


def updateGraphStats():
    sio.emit(
        "updateGraphStats", {
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "swap": psutil.swap_memory().percent,
            "time": datetime.datetime.utcnow().timestamp() * 1000
        },
        room="admins")


def updateBadgeStats():
    usageTuple = shutil.disk_usage("/")
    sio.emit(
        "updateBadgeStats", {
            "disk":
            naturalsize(usageTuple[1]),
            "disk_total":
            naturalsize(usageTuple[0]),
            "error":
            len(logs.filterLog("ERROR")) + len(logs.filterLog("CRITICAL")),
            "warning":
            len(logs.filterLog("WARNING")),
            "sites":
            0,
            "time":
            datetime.datetime.utcnow().timestamp() * 1000
        },
        room="admins")


def updateProcessStatus():
    sio.emit(
        "setProcessStatus", (process.isRunning(process.zeronetProc),
                             process.isRunning(process.spiderProc)),
        room="admins")


@sio.on("updateAll")
@apiLoginCheck
def updateAllRightNow():
    updateBadgeStats()
    updateGraphStats()
    updateProcessStatus()


def setStatus(msg):
    print("Status: " + msg)
    sio.emit("setStatus", msg)


def showMessage(type, msg):
    print(type, msg)
    sio.emit("showMessage", (type, msg), broadcast=False)


def startBroadcastingStats():
    def loop(interval, func):
        while True:
            func()
            time.sleep(interval)

    badgeThread = threading.Thread(
        target=lambda: loop(30, updateBadgeStats), daemon=True)
    statsThread = threading.Thread(
        target=lambda: loop(3, updateGraphStats), daemon=True)

    badgeThread.start()
    statsThread.start()


startBroadcastingStats()
# logs.watchLogs() # Disable log watching, use stdout instead