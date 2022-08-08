# -*- coding = utf-8 -*-
# @Time :2022/8/1 8:30
# @Author:banana889
# @File : Module.py
'''
前端调用的主要模块
'''
import datetime
import calendar
from src.backend.importModule import *
from src.backend.importance import Importance
from src.backend.state import State
from src.util.tools import *
import pickle as pk

import tinydb
# tinydb 的基本使用方法 ： https://blog.csdn.net/yangzm/article/details/82803746

class Calendar:
    def __init__(self, year, month, user):
        self.y = year
        self.m = month
        self.user = user
        self.monthTodoTable = user.todoDb.table(str(year) + str(month))
        self.monthTodo = []
        self.readFromDb()

    def readFromDb(self):
        pass

    # # 设置月份，这个影响到日历缩略图
    # def setAnsMonth(self, y, m):
    #     pass

    def getCalendar(self):
        # 二维数组
        MonthCal = calendar.monthcalendar(self.y, self.m)
        return MonthCal

    def getTasksOfMonth(self):
        # 返回一个三维列表，前两个下标和getCalendar对应，第三个下标对应这个日期的任务列表
        pass

    '''
    获取某一天的任务列表
    '''

    def getTasks(self, date: datetime.datetime):
        pass

    # datetime.datetime.now()
    def getTasksToday(self):
        pass

    def getTasksPeriod(self, date1, date2):
        pass

    def getTasksTodayAndAfter(self):
        pass

    def addTask(self):
        pass

class User:
    def __init__(self, name):
        self.name = name
        self.calendarMap = {}
        self.todoDb = db.TinyDB(DATAPATH + name + "todoDb.json")

    '''
    获取某个月的日历
    '''
    def getCalendar(self, yy, mm) -> Calendar:
        cal = Calendar(yy, mm, self)
        return cal

class Date:
    def __init__(self, date : datetime.datetime):
        self.yy = date.year
        self.mm = date.month
        self.dd = date.day
        self.taskList = []

    '''
    taskName, taskDescribe, deadline, importance
    taskDescribe, importance can be None
    '''
    def addTask(self, title, deadline: datetime.datetime, content="", importance=Importance.normal):
        newTask = Task(title, content, deadline, importance)
        self.taskList.append(newTask)
        debugPrint("added task : " + title)

    def getTasks(self):
        return self.taskList




class Task:
    def __init__(self, title: str, content: str, deadline: datetime.datetime,
                 importance=Importance.normal, state=State.notStarted):
        self.title = title
        self.content = content
        self.deadline = deadline
        self.importance = importance
        self.state = state

    def toDict(self):
        dict = {"title" : self.title,
                "content" : self.content,
                "deadline" : {"y" : self.deadline.year, "m" : self.deadline.month, "d" : self.deadline.day},
                "importance" : self.importance,
                "state" : self.state}
        return dict

    def setStart(self):
        self.state = State.inProgress

    def setFinish(self):
        self.state =State.finished
