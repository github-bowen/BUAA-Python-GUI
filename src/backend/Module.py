# -*- coding = utf-8 -*-
# @Time :2022/8/1 8:30
# @Author:banana889
# @File : Module.py
'''
前端调用的主要模块
'''
import datetime
import time

from src.backend.importModule import *
from src.backend.importance import Importance
from src.backend.state import State
from src.backend.species import Species
from src.util.tools import *
import pickle as pk

import tinydb
# tinydb 的基本使用方法 ： https://blog.csdn.net/yangzm/article/details/82803746

class Calendar:
    def __init__(self, time,  user):
        self.time = time
        self.user = user
        self.ymStr = self.time.strftime("%Y%m")
        self.monthTodoTable = user.todoDb.table(self.ymStr)
        self.monthTodo = {}
        self.readFromDb()

    def readFromDb(self):
        self.monthTodo = {}
        # 从monthTodoTable中读取，存入 monthtodo中
        for tt in self.monthTodoTable.all():
            task = Task.parseTask(tt)
            if (task.time < datetime.datetime.now()):
                self.editTask(task, newState=State.expired)
            day = task.time.day

            if day not in self.monthTodo.keys():
                self.monthTodo[day] = []
            self.monthTodo[day].append(task)

    # # 设置月份，这个影响到日历缩略图
    # def setAnsMonth(self, y, m):
    #     pass
    #
    # def getCalendar(self):
    #     # 二维数组
    #     MonthCal = calendar.monthcalendar(self.y, self.m)
    #     return MonthCal

    def getTasksOfMonth(self):
        return self.monthTodo

    '''
    获取某一天的任务列表
    '''
    def getTasksOfDay(self, date: datetime.datetime):
        # return self.monthTodoTable
        self.readFromDb() # 这里的read是为了刷新，将过期的任务标记为过期
        if date.day in self.monthTodo.keys():
            return self.monthTodo[date.day]
        return []


    # 获取一段时间内的任务
    # def getTasksPeriod(self, date1, date2):

    # 获取本月中今天以及之后的任务
    def getTasksTodayAndAfter(self):
        td = datetime.datetime.today().day
        l = []
        for k in self.monthTodo.keys():
            if k >= td:
                l = l + self.monthTodo[k]
        return l

    def addTask(self, task):
        self.monthTodoTable.insert(task.toDict())
        day = task.time.day
        if day not in self.monthTodo.keys():
            self.monthTodo[day] = []
        self.monthTodo[day].append(task)
        debugPrint("add task " + task.title)

    def deleteTask(self, task):
        day = task.time.day
        # remove from cache
        self.monthTodo[day].remove(task)
        # remove from db
        self.monthTodoTable.remove(db.where("id") == task.id)

    '''
    编辑任务
    '''

    def editTask(self, task, newTitle=None, newContent=None, newTime:datetime.datetime=None,
                 newImportance:Importance=None, newSpices=None, newState = None):

        refreshDict = {}

        # 修改task对象，记录修改
        if newTitle != None:
            task.title = newTitle
            refreshDict["title"] = newTitle
        if newContent != None:
            task.content = newContent
            refreshDict["content"] = newContent
        if newTime != None:
            task.time = newTime
            refreshDict["time"] = newTime.timestamp()
        if newImportance != None:
            task.importance = newImportance
            refreshDict["importance"] = newImportance.value
        if newSpices != None:
            task.species = newSpices
            refreshDict["species"] = newSpices.value
        if newState != None:
            task.state = newState
            refreshDict["state"] = newState.value

        # 修改数据库中的信息
        self.monthTodoTable.update(refreshDict, db.where("id") == task.id)

class User:
    def __init__(self, name):
        self.name = name
        self.calendarMap = {}
        # 一个月的代办对应一个table
        self.todoDb = db.TinyDB(DATAPATH + name + "/todoDb.json")
        self.dailyTaskTable = self.todoDb.table("daily")
        self.dailyTasks = []
        self.initDailyTask()
        # self.initCalendarMap(

    def initDailyTask(self):
        for tt in self.dailyTaskTable.all():
            dt = DailyTask.parseTask(tt)
            self.dailyTasks.append(dt)
            td = datetime.datetime.today()
            time = dt.time
            ttime = datetime.datetime(td.year, td.month, td.day, time.hour, time.minute)
            if (ttime > dt.time and dt.state != State.notStarted):
                self.editTask(dt, newState=State.notStarted, newTime=ttime)
            else:
                self.editTask(dt, newTime=ttime)

    # done
    def addTask(self, title: str, content: str, time: datetime.datetime,
                 importance=Importance.normal, state=State.notStarted, species = Species.other):
        task = Task(title, content, time, importance, state, species)
        ymStr = time.strftime("%Y%m")

        if ymStr not in self.calendarMap.keys():
            newCalender = Calendar(time, self)
            self.calendarMap[ymStr] = newCalender
        calendar_ : Calendar = self.calendarMap.get(ymStr)
        calendar_.addTask(task)

    def addDailyTask(self, title : str, content : str, startTime : datetime.datetime,
                     importance = Importance.normal, species = Species.other):
        td = datetime.datetime.today()
        startTime = datetime.datetime(td.year, td.month, td.day, startTime.hour, startTime.minute)
        dtask = DailyTask(title, content, startTime, importance, State.notStarted, species)
        self.dailyTaskTable.insert(dtask.toDict())
        self.dailyTasks.append(dtask)

    # def getTaskWithout
    # done
    def getTasksOfDay(self, day : datetime.datetime):
        ymStr = day.strftime("%Y%m")
        if self.todoDb.table(ymStr) != None:
            self.calendarMap[ymStr] = Calendar(day, self)

        if ymStr in self.calendarMap:
            calendar_:Calendar = self.calendarMap.get(ymStr)
            res =  calendar_.getTasksOfDay(day)
        else:
            res = []
        # debugPrint(str(len(res)))

        return res + self.dailyTasks

    # 获取未完成的任务
    # def getTaskUnfinished(self):
    #     pass

    # 获取 [start, end] （闭区间) 的所有代办
    def getTaskOfPeriod(self, startDay:datetime.datetime = None, endDay:datetime.datetime = None):
        tb = self.todoDb.tables()
        tb = sorted(tb)
        if (len(tb) == 0) :
            return []
        if (startDay == None):
            res = set()
            i = endDay
            assert endDay != None
            while True:
                if i.strftime("%Y%m") <tb[0]:
                    break
                res = res.union( self.getTasksOfDay(i))
                i = i + datetime.timedelta(days=-1)
            return list(res)
        elif endDay == None:
            # 获取startDay之后的
            res = set()
            i = startDay
            while True:

                if i.strftime("%Y%m") > tb[-1]:
                    break
                res = res.union( self.getTasksOfDay(i))
                i = i + datetime.timedelta(days=+1)
            return list(res)
        else:
            if endDay < startDay:
                return []
            i = startDay
            res = set()
            while i <= endDay:
                if i.strftime("%Y%m") > tb[-1]:
                    break
                res = res.union( self.getTasksOfDay(i))
                i = i + datetime.timedelta(days=+1)
            return list(res)

    def getTaskToday(self):
        return self.getTasksOfDay(datetime.datetime.today())

    # 获取本月中今天以及之后的任务
    def getTasksTodayAndAfter(self):
        ymStr = time.strftime("%Y%m")
        if ymStr not in self.calendarMap.keys():
            newCalender = Calendar(time, self)
            self.calendarMap[ymStr] = newCalender
        calendar_ : Calendar = self.calendarMap.get(ymStr)
        return calendar_.getTasksTodayAndAfter()

    # 删除任务
    def deleteTask(self, task):
        if isinstance(task, DailyTask):
            self.dailyTaskTable.remove(db.where("id") == task.id)
            self.dailyTasks.remove(task)
        else:
            ymStr = task.time.strftime("%Y%m")
            assert ymStr in self.calendarMap.keys()
            self.calendarMap[ymStr].deleteTask(task)

    '''
    编辑任务
    使用示例：user.editTask(taskToBeEdit, newTime = t) 
    '''
    def editTask(self, task, newTitle = None, newContent = None, newTime = None,
                 newImportance = None,newState = None,  newSpices = None):

        if isinstance(task, DailyTask):
            refreshDict = {}
            # 修改task对象，记录修改
            if newTitle != None:
                task.title = newTitle
                refreshDict["title"] = newTitle
            if newContent != None:
                task.content = newContent
                refreshDict["content"] = newContent
            if newTime != None:
                task.time = newTime
                if newTime > datetime.datetime.now() and task.state == State.expired and newState == None:
                    newState = State.notStarted
                refreshDict["time"] = newTime.timestamp()
            if newImportance != None:
                task.importance = newImportance
                refreshDict["importance"] = newImportance.value
            if newState != None:
                refreshDict["state"] =newState.value
            if newSpices != None:
                task.species = newSpices
                refreshDict["species"] = newSpices.value
            # 修改数据库中的信息
            self.dailyTaskTable.update(refreshDict, db.where("id") == task.id)

        else:
            ymStr = task.time.strftime("%Y%m")
            assert ymStr in self.calendarMap.keys()
            self.calendarMap[ymStr].editTask(task, newTitle, newContent, newTime, newImportance, newSpices)

    def setTaskBegin(self, task):
        # ymStr = task.time.strftime("%Y%m")
        # assert ymStr in self.calendarMap.keys()
        self.editTask(task, newState=State.inProgress)

    def setTaskEnd(self, task):
        # ymStr = task.time.strftime("%Y%m")
        # assert ymStr in self.calendarMap.keys()
        self.editTask(task, newState=State.finished)
        if isinstance(task, DailyTask):
            print(11)
            task.addFinishedDate(datetime.datetime.today())
            # self.dailyTaskTable.get()
            print(12)
            self.dailyTaskTable.update({"fd": task.toDict()["fd"]}, db.where("id") == task.id)
            print(13)

    def setTaskExpired(self, task):
        # ymStr = task.time.strftime("%Y%m")
        # assert ymStr in self.calendarMap.keys()
        self.editTask(task, newState=State.expired)

    # 根据任务的ddl和重要性调度任务，返回任务执行列表
    def scheduleTasks(self):
        ts = self.getUnstartedTasks()

        '''
        权重取决于任务的重要性和当前时间距离ddl的时间，公式暂时定为 power = importance / time
        '''
        def computePower(task):
            return task.importance.value / (task.time.timestamp() - datetime.datetime.now().timestamp())

        dict = {}
        for t in ts:
            if t.time < datetime.datetime.now():
                self.setTaskExpired(t)
                continue
            dict[t] = computePower(t)
        dict = sorted(dict.keys(), key=(lambda x : dict[x]), reverse=True)
        return list(dict)

    def getUnstartedTasks(self):
        res = self.getTaskOfPeriod(datetime.datetime.today(), None)
        res = [t for t in res if (t.state == State.notStarted)]
        return res

    # 获取已经被排布的dailyTask时间
    # def getTimeSetted(self):
    #     l = [_.time for time in ]

    def isTimeBusy(self, time : datetime.datetime):
        busyTimes = [(_.time.hour, _.time.minute) for _ in self.dailyTasks]
        if (time.hour, time.minute) in busyTimes:
            return True
        return False

    def getUnfinishTasks(self):
        res = self.getTaskOfPeriod(datetime.datetime.today(), None)
        res = [t for t in res if (t.state == State.inProgress or t.state == State.notStarted)]
        return res

    # 获取这个用户曾经添加过并且没有删除的所有任务
    def getAllTasks(self):
        res = self.getTaskOfPeriod(None, datetime.datetime.today())
        res += self.getTaskOfPeriod(datetime.datetime.today() + datetime.timedelta(days=+1), None)

        return res



# 暂且使用time 分别代表日常任务的起始时间和普通任务的结束时间
class Task:
    def __init__(self, title: str, content: str, time: datetime.datetime,
                 importance=Importance.normal, state=State.notStarted,speices=Species.work, id = -1):
        self.title = title
        self.content = content
        self.time = time
        self.importance = importance
        self.state = state
        self.species = speices
        # 每个task有唯一的编号
        if (id == -1):
            self.id = hash(title + content + str(time.timestamp()) + str(importance) + str(state) + str(speices))
        else:
            self.id = id

    def __hash__(self):
        return hash(self.id)

    @staticmethod
    def parseTask(dict):
        # dict -> Task
        time = datetime.datetime.fromtimestamp(dict["time"])
        task = Task(dict["title"], dict["content"], time, Importance(dict["importance"]),
                    State(dict["state"]), Species(dict["species"]), dict["id"])
        return task

    def toDict(self):
        dict = {"title" : self.title,
                "content" : self.content,
                "time" : self.time.timestamp(),
                "importance" : self.importance.value,
                "state" : self.state.value,
                "species" : self.species.value,
                "id" : self.id
                }
        return dict

    def setStart(self):
        self.state = State.inProgress

    def setFinish(self):
        self.state =State.finished


class DailyTask(Task):
    def __init__(self, title: str, content: str, time: datetime.datetime,
                 importance=Importance.normal, state: State = State.notStarted,speices=Species.work, id = -1,
                 finisheddate=None):
        # super(DailyTask, self).__init__()
        super().__init__(title, content, time,
                                        importance, state, speices, id)
        if finisheddate is None:
            finisheddate = set()
        self.finishEddate = finisheddate

    @staticmethod
    def parseTask(dict):
        # dict -> Task
        time = datetime.datetime.fromtimestamp(dict["time"])
        task = DailyTask(dict["title"], dict["content"], time, Importance(dict["importance"]),
                     State(dict["state"]), Species(dict["species"]), dict["id"], dict["fd"])
        print(task.__class__)
        assert isinstance(task, DailyTask)
        return task

    def toDict(self):
        d = super().toDict()
        # finishedDate
        d["fd"] = [_.timeStamp() for _ in self.finishEddate]
        return d

    def addFinishedDate(self, date : datetime.datetime):
        self.finishEddate.add(date)

    # 获取某一天的状态
    def getState(self, date):
        if (date < datetime.datetime.today()):
            if date in self.finishEddate:
                return State.finished
            return State.expired
        elif date > datetime.datetime.today():
            return State.notStarted
        else:
            return self.state
if __name__ == "__main__":
    u = User("1")
    # u.addTask("qc", "learn chapter 5", datetime.datetime(2022, 8, 20))
    # u.addTask("compiler", "final", datetime.datetime(2022, 8,20), importance=Importance.high)
    # u.addTask("数学建模", "", datetime.datetime(2022, 9, 15), importance=Importance.high)
    #
    # td = datetime.datetime.today()

    day = datetime.datetime(2022, 8, 20)

    tasks = u.getTasksOfDay(day)
    for _ in tasks:
        print(_.toDict())
    #
    # u.addTask("py hw", "backend oid calendar", datetime.datetime.today())

    # tasks = u.scheduleTasks()
    # for _ in tasks:
    #
    #     print(_.toDict())

    # u.deleteTask(tasks[2])
    # #
    # tasks = u.getTasksOfDay(td)
    # for _ in tasks:
    #
    #     print(_.toDict())

    # 测试修改任务
    # debugPrint("--测试修改任务--")
    # t = tasks[0]
    # print(t.toDict())
    # # u.editTask(t, newTitle="newTitlehaha")
    # u.setTaskEnd(t)
    # print(t.toDict())



    debugPrint("--测试dailyTask--")
    # u.addDailyTask("get up", "leave the bed", datetime.datetime(2022,1,1,hour=8))
    # tasks = u.getTasksOfDay(datetime.datetime(2022, 8 , 13))
    # tasks = u.getTaskOfPeriod(None, datetime.datetime.today())

    # tasks = set(tasks)
    # for _ in tasks:
    #     print(_.toDict())
    # dt = tasks[0]
    # u.editTask(dt, newTitle="起床起床")
    #
    # tasks = u.getTasksOfDay(datetime.datetime(2022, 8, 12))
    # for _ in tasks:
    #     print(_.toDict())


    # print(u.isTimeBusy(datetime.datetime(2222, 1,1,8,0)))
    # print(u.isTimeBusy(datetime.datetime(2222, 1,1,8,1)))


