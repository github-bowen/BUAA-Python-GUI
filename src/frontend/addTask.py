# 点击工具栏的添加按钮所显示的页面
"""
添加待办时设计的类，包括
    选择任务类型的弹窗
    添加dailyTask的子窗口
    添加normalTask的子窗口
    添加警告(在已过的日期添加)
"""
from src.backend.importance import str2Importmance
from src.backend.method import *
from PyQt5 import QtGui
from PyQt5.QtCore import QDateTime, QTime
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, \
    QGridLayout, QWidget, QMessageBox, QInputDialog, QDateTimeEdit, QTimeEdit, QTextEdit

from src.backend.species import str2Species


def showWarning(text: str):
    warningForIllegalDate = TaskAddingWarning(text)
    warningForIllegalDate.exec_()


def _checkDate(self, name: str, start:datetime, end:datetime,
               importance: str,species:str, dailyType: bool):
    if len(name.strip()) == 0:
        showWarning("\n待办名称为空，\n请重新输入！")
    elif importance.strip() == "选取":
        showWarning("\n待办重要性未选择，\n请重新选择！")
    elif species.strip() == "选取":
        showWarning("\n待办类别未选择，\n请重新选择！")
    elif dailyType and self.user.isTimeBusy(start):
        showWarning("\n 添加日常任务失败！\n 该时段已有任务哦！\n")
    elif dailyType:
        self.addDailyTask()
        self.close()
    elif start < end:
        self.addNormalTask()
        self.close()
    else:
        showWarning("添加待办失败！\n截止时间不能在当前时间之前哦！\n(*>﹏<*)")


class SelectTaskDialog(QMessageBox):  # 选择添加"日常任务"还是"一般任务"
    def __init__(self, calWindow):
        self.calWindow = calWindow
        super().__init__()
        self.setStyleSheet("QLabel{"
                             "min-width: 270px;"
                             "min-height: 260px; "
                             "}")
        self.setWindowTitle("任务管理器-待办类型选择")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setText("请选择新建待办类型：\n"
                     "日常任务为每日固定任务\n"
                     "(每天都会显示，任务时段需要在一天内)")
        font=QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.setIconPixmap(QtGui.QPixmap("../Icon/暂无记录.svg").scaled(250, 250))
        self.button_dailyTask = self.button(QMessageBox.Yes)
        self.button_normalTask = self.button(QMessageBox.No)
        self.button_dailyTask.setText("日常任务")
        self.button_normalTask.setText("一般任务")
        self.button_dailyTask.clicked.connect(self.addDaily)
        self.button_normalTask.clicked.connect(self.addNormal)

    def addDaily(self):
        self.addDailyDialog=AddDailyTaskDialog(self.calWindow.user,self.calWindow)
        self.addDailyDialog.show()

    def addNormal(self):
        self.addNormalDialog=AddNormalTaskDialog(self.calWindow.user,self.calWindow)
        self.addNormalDialog.show()


class AddTaskDialog(QWidget):
    def __init__(self, user, calWindow):
        self.calWindow = calWindow
        super().__init__()
        self.timeLE = None
        self.timeLbl = None
        self.user = user
        self.titleIcon = QLabel()
        self.titleIcon.setPixmap(QtGui.QPixmap("../Icon/名称 (1).png").scaled(40, 40))
        # self.titleIcon.setScaledContents(True)
        self.titleLbl = QLabel('日常待办名称：')
        self.titleLE = QLineEdit()

        self.contentIcon = QLabel()
        self.contentIcon.setPixmap(QtGui.QPixmap("../Icon/内容 (1).png").scaled(40, 40))
        # self.contentIcon.setScaledContents(True)
        self.contentLbl = QLabel('待办详情(可为空)：')
        self.contentTE = QTextEdit()

        self.timeIcon = QLabel()
        self.timeIcon.setPixmap(QtGui.QPixmap("../Icon/时间 (1).png").scaled(40, 40))
        # self.timeIcon.setScaledContents(True)

        self.importanceIcon = QLabel()
        self.importanceIcon.setPixmap(QtGui.QPixmap("../Icon/重要任务.png").scaled(40, 40))
        # self.importanceIcon.setScaledContents(True)
        self.importanceLbl = QLabel('重要性： ')
        self.importanceBtn = QPushButton('选取')
        self.importanceBtn.clicked.connect(self.getImportanceItem)

        self.sortIcon = QLabel()
        self.sortIcon.setPixmap(QtGui.QPixmap("../Icon/类别 (1).png").scaled(40, 40))
        # self.sortIcon.setScaledContents(True)
        self.sortLbl = QLabel('类别： ')
        self.sortBtn = QPushButton('选取')
        self.sortBtn.clicked.connect(self.getSortItem)

        self.sureBtn = QPushButton('确认')


    def dialogLayOut(self):
        dialogGrid = QGridLayout()
        dialogGrid.setSpacing(10)
        dialogGrid.addWidget(self.titleIcon, 1, 0)
        dialogGrid.addWidget(self.titleLbl, 1, 1)
        dialogGrid.addWidget(self.titleLE, 1, 2)

        dialogGrid.addWidget(self.contentIcon, 2, 0)
        dialogGrid.addWidget(self.contentLbl, 2, 1)
        dialogGrid.addWidget(self.contentTE, 2, 2)

        dialogGrid.addWidget(self.timeIcon, 3, 0)
        dialogGrid.addWidget(self.timeLbl, 3, 1)
        dialogGrid.addWidget(self.timeLE, 3, 2)

        dialogGrid.addWidget(self.importanceIcon, 4, 0)
        dialogGrid.addWidget(self.importanceLbl, 4, 1)
        dialogGrid.addWidget(self.importanceBtn, 4, 2)

        dialogGrid.addWidget(self.sortIcon, 5, 0)
        dialogGrid.addWidget(self.sortLbl, 5, 1)
        dialogGrid.addWidget(self.sortBtn, 5, 2)
        dialogGrid.addWidget(self.sureBtn, 6, 3)
        self.setLayout(dialogGrid)

    def getImportanceItem(self):
        # 创建元组并定义初始值
        items = ('灰常重要！', '普通事项', '不着急呢~')
        # 获取item输入的值，以及ok键的点击与否（True 或False）
        # QInputDialog.getItem(self,标题,文本,元组,元组默认index,是否允许更改)
        dialog = QInputDialog(self)
        # item 为 str类型
        item, ok = dialog.getItem(self, "重要性", '重要性列表', items, 0, False)

        if ok and item:
            # 满足条件时，设置选取的按钮
            self.importanceBtn.setText(item)

    def getSortItem(self):
        # 创建元组并定义初始值
        items = ('工作', '学习', '娱乐', '运动', '其他')
        # 获取item输入的值，以及ok键的点击与否（True 或False）
        # QInputDialog.getItem(self,标题,文本,元组,元组默认index,是否允许更改)
        dialog = QInputDialog()
        # item 为 str类型
        item, ok = dialog.getItem(self, "分类", '类别列表', items, 0, False)

        if ok and item:
            # 满足条件时，设置选取的按钮
            self.sortBtn.setText(item)


# 添加"日常任务"的子窗口
class AddDailyTaskDialog(AddTaskDialog):
    def __init__(self, user, calWindow):
        super().__init__(user, calWindow)
        self.initUi()
        super().dialogLayOut()

    def initUi(self):
        self.timeLbl = QLabel('起始时间：')
        self.timeLE = QTimeEdit()
        self.timeLE.setTime(QTime.currentTime())  # 设置一开始显示时的起始时间为当前时间
        self.timeLE.setDisplayFormat("hh:mm")
        self.setWindowTitle('任务管理器-创建新的日常待办')
        self.sureBtn.clicked.connect(self.checkDate)

    def addDailyTask(self):
        '''
            def addDailyTask(self, title : str, content : str, startTime : datetime.datetime,
                     importance = Importance.normal, species = Species.other):
        '''
        name, content, start, importanceStr, speciesStr = self.titleLE.text()\
            , self.contentTE.toPlainText(), self.timeLE.time()\
            , self.importanceBtn.text(), self.sortBtn.text()
        startTime = datetime.datetime(2022, 8, 13, start.hour(), start.minute())
        importance = str2Importmance[importanceStr]
        species = str2Species[speciesStr]
        #print('hhh')
        self.user.addDailyTask(name, content, startTime, importance, species)
        self.calWindow.taskDisplay(date=None, dateChange=False)  # 加完dailyTask后调用该函数刷新显示(显示的日期不变）

    def checkDate(self):
        # importanceSelected = self.importanceBtn.is
        name, start, importance, species = self.titleLE.text() \
            , self.timeLE.time(), self.importanceBtn.text(), self.sortBtn.text()
        startTime = datetime.datetime(2022, 8, 13, start.hour(), start.minute())
        _checkDate(self, name, startTime, datetime.datetime.now(), importance, species, True)


# 添加"一般任务"的子窗口
class AddNormalTaskDialog(AddTaskDialog):
    def __init__(self, user, calWindow):
        super().__init__(user, calWindow)
        self.initUi()
        super().dialogLayOut()

    def initUi(self):
        self.timeLbl = QLabel('截止日期和时间：')
        self.timeLE = QDateTimeEdit()
        self.timeLE.setDateTime(QDateTime.currentDateTime())  # 设置一开始显示时的截止时间为当前时间
        self.timeLE.setDisplayFormat("yyyy-MM-dd-hh:mm")
        self.titleLbl = QLabel('普通待办名称：')
        self.setWindowTitle('任务管理器-创建新的普通待办')
        self.sureBtn.clicked.connect(self.checkDate)

    def addNormalTask(self):
        name, content, end, importanceStr, speciesStr = self.titleLE.text(), self.contentTE.toPlainText()\
            , self.timeLE.dateTime(), self.importanceBtn.text(), self.sortBtn.text()
        importance = str2Importmance[importanceStr]
        species = str2Species[speciesStr]
        date = end.date()
        time = end.time()
        newTime = datetime.datetime(date.year(), date.month(), date.day(), time.hour(), time.minute())
        self.user.addTask(name, content, newTime, importance, species)
        self.calWindow.taskDisplay(date=None, dateChange=False)  # 加完dailyTask后调用该函数刷新显示(显示的日期不变）

    def checkDate(self):
        name, end, importance, species = self.titleLE.text() \
            , self.timeLE.dateTime(), self.importanceBtn.text(), self.sortBtn.text()
        date = end.date()
        time = end.time()
        endTime = datetime.datetime(date.year(), date.month(), date.day(), time.hour(), time.minute())
        start = datetime.datetime.now()
        _checkDate(self, name, start, endTime, importance, species, False)



class TaskAddingWarning(QMessageBox):  # 可以传入警告信息！
    def __init__(self, text):
        super().__init__()
        self.setStyleSheet("QLabel{"
                           "min-width: 240px;"
                           "min-height: 260px; "
                           "}")
        self.setText(text)
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.setIconPixmap(QtGui.QPixmap("../Icon/不小心迷路了.svg").scaled(250, 250))
        # self.setIcon(QMessageBox.Information)
        self.setWindowTitle("提示")
        self.setStandardButtons(QMessageBox.Yes)
        self.button = self.button(QMessageBox.Yes)
        self.button.setText("确定")
        self.button.clicked.connect(self.close)
