"""
添加代办时设计的类，包括
    选择任务类型的弹窗
    添加dailyTask的子窗口
    添加normalTask的子窗口
    添加警告(在已过的日期添加)
"""

import sys

from PyQt5.QtCore import QDate, QDateTime, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QApplication, QDesktopWidget, \
    QWidget, QMessageBox, QInputDialog, QMainWindow, QCalendarWidget, QFormLayout, QDateTimeEdit, QTimeEdit


def showWarning(text: str):
    warningForIllegalDate = TaskAddingWarning(text)
    warningForIllegalDate.exec_()


def _checkDate(self, name: str, start, end, importance: str):
    if len(name.strip()) == 0:
        showWarning("代办名称为空，请重新输入！")
    elif importance.strip() == "选取":
        showWarning("代办重要性未选择，请重新选择！")
    elif start < end:
        self.addDailyTask(name, start, end, importance)
        self.close()
    else:
        showWarning("添加代办失败！\n截止时间不能在起始时间前哦！\n(*>﹏<*)")


class SelectTaskDialog(QMessageBox):  # 选择添加"日常任务"还是"一般任务"
    def __init__(self):
        super().__init__()
        self.setIcon(QMessageBox.Question)
        self.setWindowTitle("代办类型选择")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setText("请选择要新建代办的类型：\n"
                     "日常任务为每日固定的任务\n"
                     "(每天都会显示，任务时段需要在一天内)")
        self.button_dailyTask = self.button(QMessageBox.Yes)
        self.button_normalTask = self.button(QMessageBox.No)
        self.button_dailyTask.setText("日常任务")
        self.button_normalTask.setText("一般任务")


# 添加"日常任务"的子窗口
class AddDailyTaskDialog(QWidget):
    def __init__(self):
        super().__init__()
        dialogGrid = QGridLayout()
        self.titleLbl = QLabel('日常待办名称：')
        self.titleLE = QLineEdit()

        self.beginTimeLbl = QLabel('起始时间：')
        self.beginTimeLE = QTimeEdit()
        self.beginTimeLE.setTime(QTime.currentTime())  # 设置一开始显示时的起始时间为当前时间
        self.endTimeLbl = QLabel('截止时间：')
        self.endTimeLE = QTimeEdit()
        self.endTimeLE.setTime(QTime.currentTime())  # 设置一开始显示时的截止时间为当前时间

        self.importanceLbl = QLabel('重要性： ')
        # self.importanceLE = QLineEdit()
        self.importanceBtn = QPushButton('选取')
        self.importanceBtn.clicked.connect(self.getItem)

        self.sureBtn = QPushButton('确认')
        dialogGrid.addWidget(self.titleLbl, 1, 0)
        dialogGrid.addWidget(self.titleLE, 1, 1)
        dialogGrid.addWidget(self.beginTimeLbl, 2, 0)
        dialogGrid.addWidget(self.beginTimeLE, 2, 1)
        dialogGrid.addWidget(self.endTimeLbl, 3, 0)
        dialogGrid.addWidget(self.endTimeLE, 3, 1)
        dialogGrid.addWidget(self.importanceLbl, 4, 0)
        # dialogGrid.addWidget(self.importanceLE, 4, 1)
        dialogGrid.addWidget(self.importanceBtn, 4, 1)
        dialogGrid.addWidget(self.sureBtn, 5, 2)
        self.setLayout(dialogGrid)
        self.setWindowTitle('创建新的日常待办')

    def getItem(self):
        # 创建元组并定义初始值
        items = ('灰常重要！', '普通事项', '并不着急')
        # 获取item输入的值，以及ok键的点击与否（True 或False）
        # QInputDialog.getItem(self,标题,文本,元组,元组默认index,是否允许更改)
        dialog = QInputDialog()
        dialog.setOkButtonText('确定')
        dialog.setCancelButtonText('取消')

        item, ok = dialog.getItem(self, "选取事项重要性", '重要性列表', items, 0, False)

        if ok and item:
            # 满足条件时，设置选取的按钮
            self.importanceBtn.setText(item)

    def addDailyTask(self, taskName: str, taskBeginTime, taskEndTime, importance):
        pass

    def checkDate(self):
        # importanceSelected = self.importanceBtn.is
        name, start, end, importance = self.titleLE.text() \
            , self.beginTimeLE.time(), self.endTimeLE.time(), self.importanceBtn.text()
        _checkDate(self, name ,start, end, importance)


# 添加"一般任务"的子窗口
class AddNormalTaskDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        dialogGrid = QGridLayout()
        self.titleLbl = QLabel('普通待办名称：')
        self.titleLE = QLineEdit()

        self.beginTimeLbl = QLabel('起始日期和时间：')
        self.beginTimeLE = QDateTimeEdit()
        self.beginTimeLE.setDateTime(QDateTime.currentDateTime())  # 设置一开始显示时的起始时间为当前时间
        self.endTimeLbl = QLabel('截止日期和时间：')
        self.endTimeLE = QDateTimeEdit()
        self.endTimeLE.setDateTime(QDateTime.currentDateTime())  # 设置一开始显示时的截止时间为当前时间

        self.importanceLbl = QLabel('重要性： ')
        # self.importanceLE = QLineEdit()
        self.importanceBtn = QPushButton('选取')
        self.importanceBtn.clicked.connect(self.getItem)

        self.sureBtn = QPushButton('确认')
        dialogGrid.addWidget(self.titleLbl, 1, 0)
        dialogGrid.addWidget(self.titleLE, 1, 1)
        dialogGrid.addWidget(self.beginTimeLbl, 2, 0)
        dialogGrid.addWidget(self.beginTimeLE, 2, 1)
        dialogGrid.addWidget(self.endTimeLbl, 3, 0)
        dialogGrid.addWidget(self.endTimeLE, 3, 1)
        dialogGrid.addWidget(self.importanceLbl, 4, 0)
        # dialogGrid.addWidget(self.importanceLE, 4, 1)
        dialogGrid.addWidget(self.importanceBtn, 4, 1)
        dialogGrid.addWidget(self.sureBtn, 5, 2)
        self.setLayout(dialogGrid)
        self.setWindowTitle('创建新的普通待办')

    def getItem(self):
        # 创建元组并定义初始值
        items = ('灰常重要！', '普通事项', '并不着急')
        # 获取item输入的值，以及ok键的点击与否（True 或False）
        # QInputDialog.getItem(self,标题,文本,元组,元组默认index,是否允许更改)
        dialog = QInputDialog()
        dialog.setOkButtonText('确定')
        dialog.setCancelButtonText('取消')

        item, ok = dialog.getItem(self, "选取事项重要性", '重要性列表', items, 0, False)

        if ok and item:
            # 满足条件时，设置选取的按钮
            self.importanceBtn.setText(item)

    def addNormalTask(self, taskName: str, taskBeginTime, taskEndTime, importance):
        pass

    def checkDate(self):
        name, start, end, importance = self.titleLE.text() \
            , self.beginTimeLE.dateTime(), self.endTimeLE.dateTime(), self.importanceBtn.text()
        _checkDate(self, name ,start, end, importance)


class TaskAddingWarning(QMessageBox):  # 可以传入警告信息！
    def __init__(self, text):
        super().__init__()
        self.setText(text)
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle("提示")
        self.setStandardButtons(QMessageBox.Yes)
        self.button = self.button(QMessageBox.Yes)
        self.button.setText("确定")
        self.button.clicked.connect(self.close)
