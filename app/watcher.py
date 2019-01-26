import time
import os

from file_read_backwards import FileReadBackwards
from flask_socketio import emit
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from app import conf


class MyHandler(FileSystemEventHandler):
    def __init__(self, on_modified=None):
        if on_modified:
            self.on_modified = on_modified

    def on_modified(self, event):
        print(
            f'Watcher event, type: {event.event_type}  path : {event.src_path}'
        )


def watch(path, *args):
    event_handler = MyHandler(*args)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()


def tailLog(path, line_count=50):
    with FileReadBackwards(path, encoding="utf-8") as frb:
        arr = []
        for _ in range(line_count):
            l = frb.readline()
            if not l:
                break
            arr.append(l)
    return arr


def watchLogs(tailLines=50):  # TODO: Send previous logs
    fz = open(conf.zeronetLogFile)
    fs = open(conf.spiderLogFile)

    fz.seek(0, os.SEEK_END)
    fs.seek(0, os.SEEK_END)

    def readMore(e):
        more = None
        if e.src_path == conf.zeronetLogFile:
            more = fz.read()
        elif e.src_path == conf.spiderLogFile:
            more = fs.read()
        if more is not None:
            emit("addLogs", more.split("\n"))

    watch(conf.zeronetLogs, readMore)
    watch(conf.spiderLogs, readMore)


if __name__ == "__main__":
    f = open("D:\\test.txt", "r")

    def readMore(e):
        more = f.read()
        if more is not None:
            print(more)

    watch("D:\\", readMore)
    time.sleep(10)
