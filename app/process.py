from app import zeronetProc, spiderProc, updateProcessStatus
from app import conf
import subprocess
import threading


def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def checkIfAlreadyRunning():
    pass


def isRunning(proc):
    return proc and proc.returncode is None


def popenAndCall(onStart, onExit, popenArgs):
    def runInThread(onStart, onExit, popenArgs):
        print("Process: {}".format(popenArgs))
        proc = subprocess.Popen(*popenArgs)
        onStart(proc)
        proc.wait()
        onExit()
        return

    thread = threading.Thread(
        target=runInThread, args=(onStart, onExit, popenArgs))
    thread.start()
    return thread


def assignZeroNetProcess(p):
    global zeronetProc
    zeronetProc = p
    updateProcessStatus()


def assignSpiderProcess(p):
    global spiderProc
    spiderProc = p
    updateProcessStatus()


def startZeroNet():
    popenAndCall(
        assignZeroNetProcess,
        updateProcessStatus,
        [[conf.python2Path, conf.zeronetRoot + "zeronet.py"] + conf.zeronetArgs
         ],
    )


def startSpider():
    popenAndCall(
        assignSpiderProcess,
        updateProcessStatus,
        [[conf.python3Path, conf.spiderRoot + "HorizonSpider.py"] +
         conf.spiderArgs],
    )