import os
from os.path import join


class Config:
    python2Path = os.getenv("python2Path", "/usr/bin/python")
    python3Path = os.getenv("python3Path", "/usr/bin/python3")
    zeronetRoot = os.getenv("zeronetRoot", "/ZeroBundle/ZeroNet/")
    zeronetLogs = os.getenv("zeronetLogs", join(zeronetRoot, "log"))
    zeronetLogFile = os.getenv("zeronetLogFile", join(zeronetLogs,
                                                      "debug.log"))
    spiderRoot = os.getenv("spiderRoot", "/HorizonSpider/")
    spiderLogs = os.getenv("spiderLogs", spiderRoot)
    spiderLogFile = os.getenv("spiderLogFile", join(spiderLogs, ".log"))
    zeronetPort = os.getenv("zeronetPort", 43110)
    spiderArgs = []
    zeronetArgs = []