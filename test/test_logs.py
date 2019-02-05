from app import logs
import pytest
from os import chdir, getcwd
import datetime

chdir("test")


@pytest.fixture
def zeronetLogFile():
    return './zeronetlog.log'


@pytest.fixture
def horizonLogFile():
    return './horizonlog.log'


def getProperDatetime(path):
    f = open(path, "r", encoding="utf-8")
    line = f.readline()
    if line:
        return logs.getDateFromLine(line)


def test_getPeriodLog(zeronetLogFile, horizonLogFile):
    znlog = logs.getPeriodLog(
        zeronetLogFile,
        (datetime.datetime.now() -
         getProperDatetime(zeronetLogFile)).total_seconds() / 3600)
    hslog = logs.getPeriodLog(
        horizonLogFile,
        (datetime.datetime.now() -
         getProperDatetime(horizonLogFile)).total_seconds() / 3600)
    assert len(znlog) > 0
    assert len(hslog) > 0


def test_isValidLogLine():
    assert logs.isValidLogLine(
        "[2019-01-25 12:46:23,644] DEBUG    TorManager > PROTOCOLINFO")
    assert not logs.isValidLogLine("250 OK")
    assert not logs.isValidLogLine(" ")
    assert not logs.isValidLogLine("")


def test_getDateFromLine():
    assert logs.getDateFromLine(
        "[2019-01-25 12:46:23,644] DEBUG    TorManager > PROTOCOLINFO")
    assert logs.getDateFromLine(" ") is None
    assert logs.getDateFromLine("") is None


def test_mixLogs():
    mixed = logs.mixLogs([
        """2019-01-06 10:19:34.138 | DEBUG    | ZiteAnalyze:analyzeFeeds:42 - Feed: 是不是感觉自己网站的网址太乱而且难记，注册bit域名可破！
,Len: 348""",
        """2019-01-06 10:19:34.179 | DEBUG    | ZiteAnalyze:extractKeyword_auto:75 - Lang of feed: zh-cn"""
    ], [
        """[2019-01-06 10:19:34,139] DEBUG    TorManager < 250 OK""",
        """[2019-01-06 10:19:34,166] DEBUG    TorManager > GETINFO version"""
    ])
    assert mixed
    assert mixed[1].startswith("[")
    assert mixed[2].startswith("[")


def test_splitLogs():
    text = """*   请先添加本站链,Len: 88
2019-01-06 10:19:32.011 | DEBUG    | ZiteAnalyze:extractKeyword_auto:75 - Lang of feed: zh-cn
2019-01-06 10:19:32.277 | DEBUG    | ZiteAnalyze:analyzeFeeds:42 - Feed: 很简单的基础问题，老司机请忽略。

* * *

找到Zer,Len: 270
2019-01-06 10:19:32.367 | DEBUG    | ZiteAnalyze:extractKeyword_auto:75 - Lang of feed: vi"""
    arr = logs.splitLogs(text)
    assert len(arr) == 3
