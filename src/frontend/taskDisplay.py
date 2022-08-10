import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, \
    QGroupBox, QLabel, QPushButton, QFormLayout, QApplication


class DisplayWidget(QWidget):
    def __init__(self, user):
        super().__init__()
        self.taskNum = 0
        self.formLayout = QFormLayout()
        self.groupBox = QGroupBox()
        self.user = user

        todayTasks = self.getTodayTask()
        self.taskNum = len(todayTasks)

        if self.taskNum > 0:
            widget = QLabel("今日代办如下：")
            font = QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setFamily("KaiTi")
            widget.setFont(font)
            self.formLayout.addRow(widget)

        for task in todayTasks:
            widget = DisplayWidget.generateTaskWidget(task)
            self.formLayout.addRow(widget)

        if self.taskNum != 0:
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
        label = QLabel("今日暂无代办哦～")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setFamily("KaiTi")
        label.setFont(font)
        self.formLayout.addWidget(label)
        self.groupBox.setLayout(self.formLayout)

    def getTodayTask(self) -> list:
        # todo: 获东西取当日所有的任务(包括未完成的)
        return [1] * 20  # todo：到时候换掉

    @staticmethod
    def generateTaskWidget(task):
        # todo: 对每一个task生成相应的Widget以便显示

        # todo: 下面随便加一些东西，测试是否有滚动条
        return QPushButton("假装这是代办(测试)")


"""
App = QApplication(sys.argv)
window = DisplayWidget(30)
sys.exit(App.exec())
"""
