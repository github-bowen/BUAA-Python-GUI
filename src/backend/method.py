# -*- coding = utf-8 -*-
# @Time :2022/8/1 14:33
# @Author:banana889
# @File : method.py
import json
from src.backend.Module import *
import os
from src.util.tools import *

ansUser: User
user2Passwd: dict = None
name2User: dict = {}

DATAPATH = "../backend/.data/"


def initialize():
    global user2Passwd
    with open(DATAPATH + "userList.json", "r") as f:
        user2Passwd = json.load(f)


def removeUesr(name: str, passwd: str):
    if (user2Passwd == None):
        initialize()
    assert name in user2Passwd.keys()
    user2Passwd[name] = None
    os.rmdir(DATAPATH + name)

    with open(DATAPATH + "userList.json", "w") as f:
        json.dump(user2Passwd, f)


def registerUser(name: str, passwd: str):
    if (user2Passwd == None):
        initialize()
    assert not name in user2Passwd.keys()
    user2Passwd[name] = passwd

    name2User[name] = User(name)

    os.mkdir(DATAPATH + name)

    # todo ������ܺ��ٴ棡
    with open(DATAPATH + "userList.json", "w") as f:
        json.dump(user2Passwd, f)


def usernameExists(username: str):
    if (user2Passwd == None):
        initialize()
    if (username in user2Passwd.keys()):
        return True
    return False


def checkPassword(username: str, password: str):
    if (not usernameExists(username)):
        return False
    if (password != user2Passwd.get(username)):
        return False
    return True

"""
返回User对象，通过调用User对象的方法获取日历信息等
"""
def loginUser(name: str, passwd: str):
    global ansUser
    if (name not in name2User.keys()):
        ansUser = User(name)
        name2User[name] = ansUser
    else:
        ansUser = name2User[name]
    return ansUser

# def getCalendar(year, month) -> Calendar:
#     pass
