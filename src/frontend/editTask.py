"""
添加编辑任务的操作窗口
与添加任务的大同小异
区别在于页面应当显示原有信息
"""

from src.backend import importance, species
from src.backend.method import *
from src.backend.importance import str2Importmance
from src.backend.species import str2Species
from PyQt5.QtWidgets import QLabel, QDateTimeEdit, QTimeEdit
import addTask

def _checkDate(self, name: str, start:datetime, end:datetime,
               importance: str,species:str, dailyType: bool):
    #dailyTime=datetime.datetime(2022,8,13,start.hour(),start.minute())
    if len(name.strip()) == 0:
        addTask.showWarning("\n待办名称为空，\n请重新输入！")
    elif importance.strip() == "选取":
        addTask.showWarning("\n待办重要性未选择，\n请重新选择！")
    elif species.strip() == "选取":
        addTask.showWarning("\n待办类别未选择，\n请重新选择！")
    elif dailyType and self.task.time.time()!=start.time() and \
            self.user.isTimeBusy(start):
        addTask.showWarning("\n 添加日常任务失败！\n 该时段已有任务哦！\n")
    elif dailyType :
        self.editDailyTask()
        self.close()
    elif start < end:
        print('1')
        self.editNormalTask()
        print('2')
        self.close()
    else:
        addTask.showWarning("添加待办失败！\n截止时间不能在当前时间之前哦！\n(*>﹏<*)")

class EditTaskDialog(addTask.AddTaskDialog):
    def __init__(self, user,calWindow,task:Task):
        super().__init__(user,calWindow)
        self.initUi(task)
        self.task=task

    def initUi(self,task:Task):
        self.titleLE.setText(task.title)
        self.contentTE.setText(task.content)
        self.importanceBtn.setText(importance.importanceDict[task.importance])
        self.sortBtn.setText(species.speciesDict[task.species])


# 修改"日常任务"的子窗口
class EditDailyTaskDialog(EditTaskDialog):
    def __init__(self, user, calenWindow, task: Task):
        super().__init__(user, calenWindow, task)
        self.timeLbl = QLabel('起始时间：')
        self.timeLE = QTimeEdit()
        # print(type(task.time.time()))
        self.timeLE.setTime(task.time.time())
        self.timeLE.setDisplayFormat("hh:mm")
        self.setWindowTitle('任务管理器-编辑日常待办')
        self.sureBtn.clicked.connect(self.checkDate)
        addTask.AddTaskDialog.dialogLayOut(self)


    def editDailyTask(self):
        '''
        def editTask(self, task, newTitle=None, newContent=None, newTime=None,
                     newImportance=None, newSpices=None):
        '''
        name, content,start, importanceStr,speciesStr = self.titleLE.text(),self.contentTE.toPlainText() \
            , self.timeLE.time(), self.importanceBtn.text(),self.sortBtn.text()
        importance=str2Importmance[importanceStr]
        species=str2Species[speciesStr]
        newTime=datetime.datetime(2022,8,13,start.hour(),start.minute())
        self.user.editTask(self.task,name,content,newTime,importance,None, species)
        #self.calWindow.refreshEvent()
        self.calWindow.taskDisplay(date=None, dateChange=False)


    def checkDate(self):
        # importanceSelected = self.importanceBtn.is
        name, start, importance,species = self.titleLE.text() \
            , self.timeLE.time(), self.importanceBtn.text(),self.sortBtn.text()
        newTime=datetime.datetime(2022,8,13,start.hour(),start.minute())
        _checkDate(self, name, newTime,datetime.datetime.now(), importance,species, True)


# 添加"一般任务"的子窗口
class EditNormalTaskDialog(EditTaskDialog):
    def __init__(self, user,calenWindow,task:Task):
        super().__init__(user,calenWindow,task)
        self.timeLbl = QLabel('截止日期和时间：')
        self.timeLE = QDateTimeEdit()
        self.timeLE.setDateTime(task.time)
        self.timeLE.setDisplayFormat("yyyy-MM-dd-hh:mm")
        self.titleLbl = QLabel('普通待办名称：')
        self.setWindowTitle('任务管理器-编辑普通待办')
        self.sureBtn.clicked.connect(self.checkDate)
        addTask.AddTaskDialog.dialogLayOut(self)

    def editNormalTask(self):
        name, content, end, importanceStr, speciesStr = self.titleLE.text(), self.contentTE.toPlainText() \
            , self.timeLE.dateTime(), self.importanceBtn.text(), self.sortBtn.text()
        importance = str2Importmance[importanceStr]
        species = str2Species[speciesStr]
        date=end.date()
        time=end.time()
        newTime=datetime.datetime(date.year(),date.month(),date.day(),time.hour(),time.minute())
        self.user.editTask(self.task,name, content, newTime, importance, None, species)
        #self.calWindow.refreshEvent()
        self.calWindow.taskDisplay(date=None, dateChange=False)

    def checkDate(self):
        name, end, importance,species = self.titleLE.text() \
            , self.timeLE.dateTime(), self.importanceBtn.text(),self.sortBtn.text()
        date = end.date()
        time = end.time()
        newTime = datetime.datetime(date.year(), date.month(), date.day(), time.hour(), time.minute())
        start = datetime.datetime.now()
        _checkDate(self, name, start, newTime, importance,species, False)
