"""
添加代办时设计的类，包括
    选择任务类型的弹窗
    添加dailyTask的子窗口
    添加normalTask的子窗口
    添加警告(在已过的日期添加)
"""
import datetime
import os
import sys

from src.backend.method import *
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QDate, QDateTime, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QApplication, QDesktopWidget, \
    QWidget, QMessageBox, QInputDialog, QMainWindow, QCalendarWidget, QFormLayout, QDateTimeEdit, QTimeEdit, QTextEdit


def showWarning(text: str):
    warningForIllegalDate = TaskAddingWarning(text)
    warningForIllegalDate.exec_()


def _checkDate(self, name: str, start, end, importance: str, dailyType: bool):
    if len(name.strip()) == 0:
        showWarning("\n代办名称为空，\n请重新输入！")
    elif importance.strip() == "选取":
        showWarning("\n代办重要性未选择，\n请重新选择！")
    elif start < end or dailyType:
        self.addDailyTask(name, start, end, importance)
        self.close()
    else:
        showWarning("添加代办失败！\n截止时间不能在当前时间之前哦！\n(*>﹏<*)")


class SelectTaskDialog(QMessageBox):  # 选择添加"日常任务"还是"一般任务"
    def __init__(self):
        super().__init__()
        self.setWindowTitle("代办类型选择")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setText("请选择要新建代办的类型：\n"
                     "日常任务为每日固定的任务\n"
                     "(每天都会显示，任务时段需要在一天内)")
        self.setIconPixmap(QtGui.QPixmap("../Icon/记录.png").scaled(250, 250))
        self.button_dailyTask = self.button(QMessageBox.Yes)
        self.button_normalTask = self.button(QMessageBox.No)
        self.button_dailyTask.setText("日常任务")
        self.button_normalTask.setText("一般任务")


class AddTaskDialog(QWidget):
    def __init__(self, username, password):
        super().__init__()
        self.user = loginUser(username, password)
        self.titleIcon = QLabel()
        self.titleIcon.setPixmap(QtGui.QPixmap("../Icon/名称.png").scaled(50, 40))
        # self.titleIcon.setScaledContents(True)
        self.titleLbl = QLabel('日常待办名称：')
        self.titleLE = QLineEdit()

        self.contentIcon = QLabel()
        self.contentIcon.setPixmap(QtGui.QPixmap("../Icon/内容.png").scaled(50, 40))
        # self.contentIcon.setScaledContents(True)
        self.contentLbl = QLabel('待办详情(可为空)：')
        self.contentTE = QTextEdit()

        self.timeIcon = QLabel()
        self.timeIcon.setPixmap(QtGui.QPixmap("../Icon/时间.png").scaled(50, 40))
        # self.timeIcon.setScaledContents(True)

        self.importanceIcon = QLabel()
        self.importanceIcon.setPixmap(QtGui.QPixmap("../Icon/等级.png").scaled(50, 40))
        # self.importanceIcon.setScaledContents(True)
        self.importanceLbl = QLabel('重要性： ')
        self.importanceBtn = QPushButton('选取')
        self.importanceBtn.clicked.connect(self.getImportanceItem)

        self.sortIcon = QLabel()
        self.sortIcon.setPixmap(QtGui.QPixmap("../Icon/类别.png").scaled(50, 40))
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
        items = ('灰常重要！', '普通事项', '并不着急')
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
        items = ('工作', '学习', '娱乐','运动','其他')
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
    def __init__(self, username, password):
        super().__init__(username, password)
        self.initUi()
        super().dialogLayOut()

    def initUi(self):
        self.timeLbl = QLabel('起始时间：')
        self.timeLE = QTimeEdit()
        self.timeLE.setTime(QTime.currentTime())  # 设置一开始显示时的起始时间为当前时间
        self.setWindowTitle('创建新的日常待办')

    '''
    def addTask(self, title: str, content: str, deadline: datetime.datetime,
                importance=Importance.normal, state=State.notStarted):

    def addDailyTask(self):
        name, time, content, importance,species = self.titleLE.text() \
            , self.beginTimeLE.time(), self.endTimeLE.time(), self.importanceBtn.text()\
            ,self.sortLE.text()
        self.user.addTask(name,content,end)
     '''

    def addDailyTask(self):
        pass

    def checkDate(self):
        # importanceSelected = self.importanceBtn.is
        name, start, importance = self.titleLE.text() \
            , self.timeLE.time(), self.importanceBtn.text()
        end = 0
        _checkDate(self, name, start, end, importance, True)


# 添加"一般任务"的子窗口
class AddNormalTaskDialog(AddTaskDialog):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.initUi()
        super().dialogLayOut()

    def initUi(self):
        self.timeLbl = QLabel('截止日期和时间：')
        self.timeLE = QDateTimeEdit()
        self.timeLE.setDateTime(QDateTime.currentDateTime())  # 设置一开始显示时的截止时间为当前时间
        self.titleLbl = QLabel('普通待办名称：')
        self.setWindowTitle('创建新的普通待办')

    def addNormalTask(self, taskName: str, taskBeginTime, taskEndTime, importance):
        pass

    def checkDate(self):
        name, end, importance = self.titleLE.text() \
            , self.timeLE.dateTime(), self.importanceBtn.text()
        start = datetime.datetime.now()
        _checkDate(self, name, start, end, importance, False)


class TaskAddingWarning(QMessageBox):  # 可以传入警告信息！
    def __init__(self, text):
        super().__init__()
        self.setText(text)
<<<<<<< HEAD
        self.setIconPixmap(QtGui.QPixmap("../Icon/加载失败.png").scaled(150, 150))
        # self.setIcon(QMessageBox.Information)
=======
        self.setIconPixmap(QtGui.QPixmap("../Icon/不小心迷路了.png").scaled(250, 250))
        #self.setIcon(QMessageBox.Information)
>>>>>>> dev
        self.setWindowTitle("提示")
        self.setStandardButtons(QMessageBox.Yes)
        self.button = self.button(QMessageBox.Yes)
        self.button.setText("确定")
        self.button.clicked.connect(self.close)
