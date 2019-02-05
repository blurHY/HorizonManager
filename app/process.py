from . import main, conf

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
            proc = subprocess.Popen(*popenArgs)
            onStart(proc)
            proc.wait()
            onExit()
        except Exception as e:
            print(e)
            main.showMessage("error", "Failed to start process")
        return

    thread = threading.Thread(
        target=runInThread, args=(onStart, onExit, popenArgs))
    thread.daemon = True
    thread.start()
    return thread


@checkIfAlreadyRunning(zeronetProc)
def startZeroNet():
    def assignZeroNetProcess(p):
        global zeronetProc
        zeronetProc = p
        main.updateProcessStatus()

    popenAndCall(
        assignZeroNetProcess,
        main.updateProcessStatus,
        [[conf.python2Path, conf.zeronetRoot + "zeronet.py"] + conf.zeronetArgs
         ],
    )


@checkIfAlreadyRunning(spiderProc)
def startSpider():
    def assignSpiderProcess(p):
        global spiderProc
        spiderProc = p
        main.updateProcessStatus()

    popenAndCall(
        assignSpiderProcess,
        main.updateProcessStatus,
        [[conf.python3Path, conf.spiderRoot + "HorizonSpider.py"] +
         conf.spiderArgs],
    )