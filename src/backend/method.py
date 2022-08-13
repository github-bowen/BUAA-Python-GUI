# -*- coding = utf-8 -*-
# @Time :2022/8/1 14:33
# @Author:banana889
# @File : method.py
import os

import tinydb
from src.backend.Module import *
from src.backend.importModule import *
from src.util.tools import *

ansUser = None
user2Passwd : db.TinyDB = None
name2User: dict = {}



def initialize():
    global user2Passwd
    # with open(DATAPATH + "userList.json", "r") as f:
    if not os.path.exists(DATAPATH):
        os.mkdir(DATAPATH)
    user2Passwd = db.TinyDB(DATAPATH + "userList.json")


def removeUesr(name: str, passwd: str):
    if (user2Passwd == None):
        initialize()


    q = db.Query()
    assert user2Passwd.contains(q.name == name)
    user2Passwd.remove(q.name == name)
    os.remove(DATAPATH + name)

def registerUser(name: str, passwd: str):
    if (user2Passwd == None):
        initialize()
    assert not usernameExists(name)

    user2Passwd.insert({"name" : name, "passwd" : passwd})

    if (not os.path.exists(DATAPATH + name)):
        os.mkdir(DATAPATH + name)
    with open(DATAPATH + name + "/todoDb.json", "w"):
        pass

    # todo 数据加密储存


def usernameExists(username: str):
    q = db.Query()
    if (user2Passwd == None):
        initialize()
    if (user2Passwd.contains(q.name == username)):
        return True
    return False

def checkPassword(username: str, password: str):
    q = db.Query()
    if (not usernameExists(username)):
        return False
    if (password != user2Passwd.get(q.name == username)["passwd"]):
        return False
    return True

"""
返回User对象，通过调用User对象的方法获取日历信息等
"""
def loginUser(name: str, passwd: str):
    global ansUser
    name = name.strip()
    debugPrint(name)
    if (not usernameExists(name)):
        debugWarning("you are logging in a unregistered User!")
    if (name not in name2User.keys()):
        ansUser = User(name)
        name2User[name] = ansUser
    else:
        ansUser = name2User[name]
    return ansUser

def setPasswd(name, new):
    q = db.Query()
    user2Passwd.update({"passwd": new}, db.where('name') == name)

if __name__ == "__main__":
    # registerUser("hi", "hi")
    removeUesr("hi", "hi")
    # u = loginUser("ba", "na")
    # setPasswd("ba", "ba")

    # tb = db.TinyDB(DATAPATH + "ba/todoDb.json")
    # with open(DATAPATH + "userList.json") as f:
    #     print(f.readline())