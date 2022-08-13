import datetime
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, \
    QGroupBox, QLabel, QPushButton, QFormLayout, QApplication

from TaskLabel import TaskLabel


class DisplayWidget(QWidget):
    def __init__(self, user):
        super().__init__()
        self.taskNum = 0
        self.formLayout = QFormLayout()
        self.groupBox = QGroupBox()
        self.user = user
        self.allTasks = None
        self.displayingDate = datetime.datetime.now()

        self.todayTasks = self.getTodayTask()
        self.displayingTasks = self.todayTasks
        self.taskNum = len(self.todayTasks)

        if self.taskNum > 0:
            widget = QLabel("今日待办如下：")
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            # font.setFamily("KaiTi")
            widget.setFont(font)
            self.formLayout.addRow(widget)

            for task in self.todayTasks:
                widget = self.generateTaskWidget(task)
                self.formLayout.addRow(widget)
            self.groupBox.setLayout(self.formLayout)
        else:
            self.displayNoTaskToday()

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.groupBox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(400)  # 对应CalenWindow高度
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll)
        self.show()

    def refreshAndDisplay(self, date, dateChanged: bool):
        self.close()
        self.formLayout = QFormLayout()
        self.groupBox = QGroupBox()

        if dateChanged:
            self.displayingDate = date
            self.displayingTasks = self.getTaskOfDate(date)
        else:
            self.displayingTasks = self.getTaskOfDate(self.displayingDate)
        self.taskNum = len(self.todayTasks)

        if self.taskNum > 0:
            widget = QLabel("今日待办如下：")
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            # font.setFamily("KaiTi")
            widget.setFont(font)
            self.formLayout.addRow(widget)

            for task in self.todayTasks:
                widget = self.generateTaskWidget(task)
                self.formLayout.addRow(widget)
            self.groupBox.setLayout(self.formLayout)
        else:
            self.displayNoTaskToday()

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.groupBox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(400)  # 对应CalenWindow高度
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll)
        self.show()

    def displayNoTaskToday(self):  # 显示下面的提示文字
        label = QLabel("今日暂无待办哦～")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        # font.setFamily("KaiTi")
        label.setFont(font)
        self.formLayout.addWidget(label)
        self.groupBox.setLayout(self.formLayout)

    def getTodayTask(self) -> list:
        return self.user.getTaskToday()

    def generateTaskWidget(self, task):
        taskLabel = TaskLabel(task=task, user=self.user)
        return taskLabel

    def getAllDateTasks(self) -> list:
        return self.user.getAllTasks()

    def getTaskOfDate(self, date):
        return self.user.getTasksOfDay(date)


"""
App = QApplication(sys.argv)
window = DisplayWidget(30)
sys.exit(App.exec())
"""
