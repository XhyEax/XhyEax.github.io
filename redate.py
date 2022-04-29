import os
import time

from pywintypes import Time  # 可以忽视这个 Time 报错（运行程序还是没问题的）
from win32file import (GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING, CloseHandle,
                       CreateFile, GetFileTime, SetFileTime)


def modifyFileTime(filePath, createTime, modifyTime, accessTime):
    """
    用来修改任意文件的相关时间属性，时间格式：YYYY-MM-DD HH:MM:SS 例如：2019-02-02 00:01:02
    :param filePath: 文件路径名
    :param createTime: 创建时间
    :param modifyTime: 修改时间
    :param accessTime: 访问时间
    :param offset: 时间偏移的秒数,tuple格式，顺序和参数时间对应
    """
    format = "%Y-%m-%dT%H:%M:%S"  # 时间格式
    cTime_t = timeOffsetAndStruct(createTime, format)
    mTime_t = timeOffsetAndStruct(modifyTime, format)
    aTime_t = timeOffsetAndStruct(accessTime, format)

    fh = CreateFile(filePath, GENERIC_READ | GENERIC_WRITE,
                    0, None, OPEN_EXISTING, 0, 0)
    createTimes, accessTimes, modifyTimes = GetFileTime(fh)

    createTimes = Time(time.mktime(cTime_t))
    accessTimes = Time(time.mktime(aTime_t))
    modifyTimes = Time(time.mktime(mTime_t))
    SetFileTime(fh, createTimes, accessTimes, modifyTimes)
    CloseHandle(fh)


def timeOffsetAndStruct(times, format):
    return time.localtime(time.mktime(time.strptime(times, format)))


def redate(path):
    startstr = "date: "
    startstr_len = len(startstr)
    time_len = len("15:20:05")

    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            filename, extname = os.path.splitext(name)
            if(".md" in extname):
                filepath = os.path.join(root, name)
                print(filepath)
                createTime = ""
                with open(filepath, "r", encoding="utf-8") as f:
                    data = f.read()
                    start = data.index(startstr)
                    end = data.find("T", start)
                    createTime = data[start+startstr_len:end+1+time_len]
                print(createTime)
                mTime = createTime
                aTime = createTime
                modifyFileTime(filepath, createTime, mTime, aTime)


# redate("D:\Blog\source\_drafts")
redate("D:\Blog\source\_posts")
