"""
添加编辑任务的操作窗口
与添加任务的大同小异
区别在于页面应当显示原有信息
"""
from src.backend import importance, species
from src.backend.method import *
from PyQt5.QtWidgets import QLabel, QDateTimeEdit, QTimeEdit
import addTask

def _checkDate(self, name: str, start, end, importance: str, dailyType: bool):
    if len(name.strip()) == 0:
        addTask.showWarning("\n待办名称为空，\n请重新输入！")
    elif importance.strip() == "选取":
        addTask.showWarning("\n待办重要性未选择，\n请重新选择！")
    # TODO:后端需要提供日常任务排布时间的list，返回bool值，def dailyTimeSetted(time:datetime)
    # elif dailyType and dailyTimeSetted(start):
    # showWarning("\n 添加日常任务失败！\n 该时段已有任务哦！\n")
    elif dailyType :
        self.editDailyTask(name, start, end, importance)
        self.close()
    elif  start < end:
        self.editNormalTask(name, start, end, importance)
        self.close()
    else:
        addTask.showWarning("添加待办失败！\n截止时间不能在当前时间之前哦！\n(*>﹏<*)")

class EditTaskDialog(addTask.AddTaskDialog):
    def __init__(self, username, password,task:Task):
        super().__init__(username, password)
        self.initUi(task)

    def initUi(self,task:Task):
        self.titleLE.setText(task.title)
        self.contentTE.setText(task.content)
        self.importanceBtn.setText(importance.importanceDict[task.importance])
        self.sortBtn.setText(species.speciesDict[task.species])

# 修改"日常任务"的子窗口
class EditDailyTaskDialog(EditTaskDialog):
    def __init__(self, username, password,task):
        super().__init__(username, password,task)
        self.timeLbl = QLabel('起始时间：')
        self.timeLE = QTimeEdit()
        # print(type(task.time.time()))
        self.timeLE.setTime(task.time.time())
        self.timeLE.setDisplayFormat("hh:mm")
        self.setWindowTitle('编辑日常待办')
        self.sureBtn.clicked.connect(self.checkDate)
        addTask.AddTaskDialog.dialogLayOut(self)

    def editDailyTask(self):
        # 删去原有记录，添加新纪录
        # TODO：后端需添加接口
        pass

    def checkDate(self):
        # importanceSelected = self.importanceBtn.is
        name, start, importance = self.titleLE.text() \
            , self.timeLE.time(), self.importanceBtn.text()
        end = 0
        _checkDate(self, name, start, end, importance, True)


# 添加"一般任务"的子窗口
class EditNormalTaskDialog(EditTaskDialog):
    def __init__(self, username, password,task:Task):
        super().__init__(username, password,task)
        self.timeLbl = QLabel('截止日期和时间：')
        self.timeLE = QDateTimeEdit()
        self.timeLE.setDateTime(task.time)
        self.timeLE.setDisplayFormat("yyyy-mm-dd-hh:mm")
        self.titleLbl = QLabel('普通待办名称：')
        self.setWindowTitle('编辑普通待办')
        self.sureBtn.clicked.connect(self.checkDate)
        addTask.AddTaskDialog.dialogLayOut(self)

    def editNormalTask(self, taskName: str, taskBeginTime, taskEndTime, importance):
        # TODO:与上同理
        pass

    def checkDate(self):
        name, end, importance = self.titleLE.text() \
            , self.timeLE.dateTime(), self.importanceBtn.text()
        start = datetime.datetime.now()
        _checkDate(self, name, start, end, importance, False)
