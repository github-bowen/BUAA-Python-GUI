# -*- coding = utf-8 -*-
# @Time :2022/8/1 8:30
# @Author:banana889
# @File : Module.py
'''
前端调用的主要模块
'''
import datetime
import calendar
from importance import Importance
from state import State

class User:
    pass

class Calendar:
    def __init__(self, year, month, user):
        self.y = year
        self.m = month
        self.user = user

    # 设置月份，这个影响到日历缩略图
    def setAnsMonth(self, y, m):
        pass

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


class Date:
    '''
    taskName, taskDescribe, deadline, importance
    taskDescribe, importance can be None
    '''

    def addTask(taskName, deadline: datetime.datetime, taskDescribe="", importance: int = 0):
        pass


class Task:
    def __init__(self, title: str, content: str, deadline: str,
                 importance=Importance.normal, state=State.notStarted):
        self.title = title
        self.content = content
        self.deadline = deadline
        self.importance = importance
        self.state = state




