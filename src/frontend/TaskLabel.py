import sys
from datetime import datetime

from PyQt5.QtCore import pyqtSignal

from src.backend.Module import Task
from src.backend.importance import *
import addTask
import editTask

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout, \
    QApplication, QWidget, QCheckBox, QMessageBox, QTimeEdit

from src.backend.method import loginUser
from src.backend.species import Species
from src.backend.state import stateDict
from src.frontend.qssLoader import QSSLoader


class TaskLabel(QWidget):
    def __init__(self, task: Task, user, calenWindow):
        super().__init__()
        self.calenWindow = calenWindow
        # self.user = loginUser(username, password)
        self.user = user
        self.task = task
        self.initUi()

    def initUi(self):
        state = self.task.state
        title = self.task.title
        importance = self.task.importance
        species = self.task.species
        time = self.task.time
        self.stateLabel = QLabel(stateDict[state])
        self.nameLabel = QLabel(title)

        # 由重要性和种类得图标颜色
        self.icon = QLabel()
        iconName = str(species)
        if importance == Importance.high:
            iconName = iconName + " (2)"
        elif importance == Importance.normal:
            iconName = iconName + " (3)"
        elif importance == Importance.low:
            iconName = iconName + " (1)"
        else:
            addTask.showWarning("重要性传入有误!")
        self.icon.setPixmap(QPixmap("../Icon/taskSort/%s.png" % iconName).scaled(50, 50))

        # 控制格式
        timeStr = "{:02d}:{:02d}".format(time.hour, time.minute)
        self.timeLabel = QLabel(timeStr)

        self.editBtn = QPushButton('编辑')

        # 开始只有按下和弹起两种状态
        self.beginBtn = QPushButton('开始')
        self.beginBtn.setCheckable(True)
        self.beginBtn.clicked[bool].connect(self.beginThing)

        self.finishBtn = QCheckBox('完成', self)
        self.finishBtn.toggle()
        self.finishBtn.setChecked(False)

        self.finishBtn.clicked.connect(self.finishThing)

        '''
        下为按钮模式
        self.finshBtn=QPushButton('完成')
        self.finshBtn.clicked.connect(self.finshThing)
        '''
        self.deleteBtn = QPushButton()
        self.deleteBtn.setIcon(QIcon("../Icon/删除.png"))
        self.deleteMsg = deletWindow(title)
        self.deleteBtn.clicked.connect(self.deleteMsg.show)
        self.deleteMsg.button(QMessageBox.Yes).clicked.connect(self.deleteThing)

        self.taskLayOut()
        self.show()

    def taskLayOut(self):
        self.taskGrid = QGridLayout(self)
        self.taskGrid.addWidget(self.icon, 0, 0)
        self.taskGrid.addWidget(self.stateLabel, 0, 1)
        self.taskGrid.addWidget(self.nameLabel, 0, 2)
        self.taskGrid.addWidget(self.timeLabel, 0, 3)
        self.taskGrid.addWidget(self.editBtn, 0, 4)
        self.taskGrid.addWidget(self.beginBtn, 0, 5)
        self.taskGrid.addWidget(self.finishBtn, 0, 6)
        self.taskGrid.addWidget(self.deleteBtn, 0, 7)
        self.setLayout(self.taskGrid)

    def beginThing(self):
        self.user.setTaskBegin(self.task)
        self.stateLabel.setText(stateDict[self.task.state])
        # todo 记录开始时间？

    def finishThing(self):
        # TODO：同时触发calenderFront的taskDisplay函数
        if not self.beginBtn.isChecked():
            addTask.showWarning("\n 当前任务尚未开始\n 无法完成哦")
            self.finishBtn.setChecked(False)
        else:
            self.finishMsg = finishWindow(self.task.title)
            self.finishMsg.show()
            self.finishMsg.button(QMessageBox.Yes).clicked.connect(self.canFinish)
            self.finishMsg.button(QMessageBox.No).clicked.connect(self.cancelFinish)


    def canFinish(self):
        self.user.setTaskEnd(self.task)
        self.stateLabel.setText(stateDict[self.task.state])
        self.calenWindow.taskDisplay(None, False)

    def cancelFinish(self):
        self.finishBtn.setChecked(False)


    def deleteThing(self):
        self.user.deleteTask(self.task)
        self.calenWindow.taskDisplay(None, False)

class finishWindow(QMessageBox):
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle("确认完成操作")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setText("确认完成待办\n \"%s\" 吗？" % title)
        self.setIconPixmap(QPixmap("../Icon/记录.png").scaled(250, 250))
        self.sureBtn = self.button(QMessageBox.Yes)
        self.sureBtn.setText("确认")
        self.cancelBtn = self.button(QMessageBox.No)
        self.cancelBtn.setText("我再想想")


class deletWindow(QMessageBox):
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle("确认删除操作")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setText("确认删除待办\n \"%s\" 吗？" % title)
        self.setIconPixmap(QPixmap("../Icon/记录.png").scaled(250, 250))
        self.sureBtn = self.button(QMessageBox.Yes)
        self.sureBtn.setText("确认")
        self.cancelBtn = self.button(QMessageBox.No)
        self.cancelBtn.setText("我再想想")


class dailyTaskLabel(TaskLabel):
    def __init__(self, username, password, task: Task):
        super().__init__(task, username, password)
        self.editDailyTaskDialog = editTask.EditDailyTaskDialog(username, password, task)
        self.editDailyTaskDialog.sureBtn.clicked.connect(self.editDailyTaskDialog.checkDate)
        self.editBtn.clicked.connect(self.editDailyTaskDialog.show)


class normalTaskLabel(TaskLabel):
    def __init__(self, username, password, task: Task):
        super().__init__(task, username, password)
        self.editNormalTaskDialog = editTask.EditNormalTaskDialog(username, password, task)
        self.editBtn.clicked.connct(self.editNormalTaskDialog.show)
        self.editNormalTaskDialog.sureBtn.clicked.connect(self.editNormalTaskDialog.checkDate)


# 测试
if __name__ == "__main__":
    app = QApplication(sys.argv)
    date = datetime.now()
    task = Task('检查', '', date, importance=Importance.normal, speices=Species.sport)
    text = dailyTaskLabel('kl', 'zjtdbd', task)
    app.exec_()
