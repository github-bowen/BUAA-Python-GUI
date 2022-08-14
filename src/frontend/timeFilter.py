# 点击工具栏的筛选按钮所显示的页面
import datetime
import sys

from src.backend.method import *
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QDate, QDateTime, QTime
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtWidgets import qApp, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QApplication, QDesktopWidget, \
    QWidget, QMessageBox, QInputDialog, QMainWindow, QCalendarWidget, QFormLayout, QDateTimeEdit, QTimeEdit, QTextEdit, \
    QGroupBox, QScrollArea

from src.frontend import addTask
from src.frontend.TaskLabel import DailyTaskLabel, NormalTaskLabel


class TimeFilter(QWidget):
    def __init__(self, user, calenWindow):
        super().__init__()
        self.user = user
        self.calenWindow = calenWindow
        self.initUi()
        self.timeFliterLayOut()

    def initUi(self):
        self.titleLbl = QLabel('筛选相应时间段的任务')
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setFamily("KaiTi")
        self.titleLbl.setFont(font)
        self.beginLbl = QLabel('请选取起始时间:')
        self.beginIcon = QLabel()
        self.beginIcon.setPixmap(QPixmap("../Icon/时间.png").scaled(50, 40))
        self.beginTE = QDateTimeEdit()
        self.beginTE.setDateTime(QDateTime.currentDateTime())
        self.beginTE.setDisplayFormat("yyyy-MM-dd-hh:mm")
        self.endLbl = QLabel('请选取截止时间:')
        self.endIcon = QLabel()
        self.endIcon.setPixmap(QPixmap("../Icon/时间 (1).png").scaled(50, 40))
        self.endTE = QDateTimeEdit()
        self.endTE.setDateTime(QDateTime.currentDateTime())
        self.endTE.setDisplayFormat("yyyy-MM-dd-hh:mm")
        self.sureBtn = QPushButton('确定')
        self.sureBtn.clicked.connect(self.checkDateAndDisplay)
        # todo:显示一个taskDisplay
        self.cancelBtn = QPushButton('取消')
        self.cancelBtn.clicked.connect(self.close)

    def timeFliterLayOut(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.titleLbl, 0, 0, 2, 1)
        self.form = QFormLayout()
        self.form.addRow(self.beginIcon, self.beginLbl)
        self.form.addRow(self.beginTE)
        self.form.addRow(self.endIcon, self.endLbl)
        self.form.addRow(self.endTE)
        self.grid.addLayout(self.form, 4, 0)
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.sureBtn)
        self.hbox.addWidget(self.cancelBtn)
        self.grid.addLayout(self.hbox, 5, 0)
        self.setLayout(self.grid)

    def checkDateAndDisplay(self):
        begin, end = self.beginTE.dateTime(), self.endTE.dateTime()
        if begin >= end:
            addTask.showWarning("起始日期不能超\n"
                                "过截止日期哦～")
        else:
            beginDate, beginTime = begin.date(), begin.time()
            endDate, endTime = end.date(), end.time()
            beginDatetime = datetime.datetime(
                beginDate.year(), beginDate.month(), beginDate.day(),
                beginTime.hour(), beginTime.minute())
            endDatetime = datetime.datetime(
                endDate.year(), endDate.month(), endDate.day(),
                endTime.hour(), endTime.minute())
            print("before creating TimeFilterDisplay")
            self.timeFilterDisplay = TimeFilterDisplay(
                self.user, beginDatetime, endDatetime, self.calenWindow)
            self.timeFilterDisplay.layout = QVBoxLayout(self.timeFilterDisplay)
            self.timeFilterDisplay.layout.addWidget(self.timeFilterDisplay.scroll)
            self.tempWidget = QWidget()
            self.tempWidget.setLayout(self.timeFilterDisplay.layout)
            self.tempWidget.show()


            print("after creatingTimeFilterDisplay")
            self.close()


class TimeFilterDisplay(QMainWindow):
    def __init__(self, user, beginDatetime: datetime.datetime,
                 endDatetime: datetime.datetime, calenWindow):
        super(TimeFilterDisplay, self).__init__()
        self.scroll = QScrollArea()
        self.user = user
        self.beginDatetime = beginDatetime
        self.endDatetime = endDatetime
        self.calenWindow = calenWindow
        self.displayingTasks = None
        self.initUI()

    def initUI(self):
        self.formLayout = QFormLayout()
        self.groupBox = QGroupBox()

        self.displayingTasks = self.user.getTaskOfPeriod(
            self.beginDatetime, self.endDatetime)
        self.taskNum = len(self.displayingTasks)

        if self.taskNum > 0:
            widget = QLabel(str(self.beginDatetime)
                            + "到" + str(self.endDatetime) + "的待办如下：")
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            # font.setFamily("KaiTi")
            widget.setFont(font)
            self.formLayout.addRow(widget)

            titleFont = QFont()
            titleFont.setBold(True)
            titleWidget = QWidget()
            hbox = QHBoxLayout()
            sortLabel = QLabel('类别')
            stateLabel = QLabel('状态')
            nameLabel = QLabel('名称')
            timeLabel = QLabel('时间')
            sortLabel.setFont(titleFont)
            stateLabel.setFont(titleFont)
            nameLabel.setFont(titleFont)
            timeLabel.setFont(titleFont)

            hbox.addWidget(sortLabel)
            hbox.addWidget(stateLabel)
            hbox.addWidget(nameLabel)
            hbox.addWidget(timeLabel)
            for i in range(4):
                hbox.addWidget(QLabel())
            titleWidget.setLayout(hbox)
            self.formLayout.addRow(titleWidget)

            for task in self.displayingTasks:
                widget = self.generateTaskWidget(task)
                self.formLayout.addRow(widget)
            self.groupBox.setLayout(self.formLayout)
        else:
            label = QLabel(str(self.beginDatetime)
                           + "到" + str(self.endDatetime) + "暂无待办哦～")
            font = QFont()
            font.setPointSize(16)
            font.setBold(True)
            # font.setFamily("KaiTi")
            label.setFont(font)

            self.formLayout.addWidget(label)
            self.formLayout.addWidget(QLabel())
            self.groupBox.setLayout(self.formLayout)

        # self.disableHorizontalScroll()
        self.scroll.setWidget(self.groupBox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(400)  # 对应CalenWindow高度
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll)
        # self.show()

    def generateTaskWidget(self, task: Task):
        if isinstance(task, DailyTask):
            taskLabel = DailyTaskLabel(date=task.time, task=task, user=self.user,
                                       calenWindow=self.calenWindow)
        else:
            taskLabel = NormalTaskLabel(task=task, user=self.user, calenWindow=self.calenWindow)
        return taskLabel
