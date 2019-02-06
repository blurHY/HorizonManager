from . import main, conf, sio, logs

import os
import subprocess
import threading

spiderProc = None
zeronetProc = None


def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def checkIfAlreadyRunning(proc):  # TODO: Check port and lock file
    def decorate(func):
        def wrapper(*args, **kwargs):
            if isRunning(proc):
                main.showMessage("error", "The process is already running")
            else:
                func(*args, **kwargs)

        return wrapper

    return decorate


def isRunning(proc):
    return proc and proc.returncode is None


def popenAndCall(onStart, onExit, popenArgs):
    def runInThread(onStart, onExit, popenArgs):
        print("Process: {}".format(popenArgs))
        try:
            proc = subprocess.Popen(
                *popenArgs,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            onStart(proc)
            proc.wait()
            onExit()
        except Exception as e:
            print(e)
            main.showMessage("error", "Failed to start process")
        else:
            main.showMessage("success", f"{popenArgs} started")
        return

    thread = threading.Thread(
        target=runInThread, args=(onStart, onExit, popenArgs))
    thread.start()
    return thread


@checkIfAlreadyRunning(zeronetProc)
def startZeroNet():
    def gotZeroNetProc(p):
        global zeronetProc
        zeronetProc = p
        main.updateProcessStatus()
        startStdoutWatcher(p)

    popenAndCall(
        gotZeroNetProc,
        main.updateProcessStatus,
        [[conf.python2Path,
          os.path.join(conf.zeronetRoot, "zeronet.py")] + conf.zeronetArgs],
    )


@checkIfAlreadyRunning(spiderProc)
def startSpider():
    def gotSpiderProc(p):
        global spiderProc
        spiderProc = p
        main.updateProcessStatus()
        startStdoutWatcher(p)

    popenAndCall(
        gotSpiderProc,
        main.updateProcessStatus,
        [[conf.python3Path,
          os.path.join(conf.spiderRoot, "HorizonSpider.py")] + conf.spiderArgs
         ],
    )


def startStdoutWatcher(proc):
    def loop():
        while True:
            output = proc.stdout.readline().decode("utf-8")
            err = proc.stderr.readline().decode("utf-8")
            if output == '' and err == "" \
             and proc.poll() is not None and not isRunning(proc):
                break
            sio.emit(
                "addLogs",
                logs.mixLogs(logs.splitLogs(output), logs.splitLogs(err)),
                room="admins")

        main.updateProcessStatus()

    thread = threading.Thread(daemon=True, target=loop)
    thread.start()
    print(f"Stdout watcher for {proc} started")