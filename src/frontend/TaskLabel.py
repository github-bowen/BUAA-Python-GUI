# 未完成 进行中 已完成 已过期
# 未完成和已过期显示开始
# 进行中和已完成显示结束

from PyQt5.QtCore import Qt

from src.backend.Module import Task, DailyTask
from src.backend.importance import *
import addTask
import editTask

from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout, \
     QWidget, QCheckBox, QMessageBox
from src.backend.state import stateDict, State


class TaskLabel(QWidget):
    def __init__(self, task: Task, user, calenWindow, date=None):
        super().__init__()
        self.deleteBtn = None
        self.switchBtn = None
        self.editBtn = None
        self.timeLabel = None
        self.nameLabel = None
        self.stateLabel = None
        self.calenWindow = calenWindow
        self.user = user
        self.task = task
        self.date = date
        self.initUi()

    def initUi(self):
        state = self.task.state
        if isinstance(self.task, DailyTask) and self.date is not None:
            state = self.task.getState(self.date)
        title = self.task.title
        content = self.task.content
        importance = self.task.importance
        species = self.task.species
        time = self.task.time

        self.stateLabel = QLabel(stateDict[state])
        self.stateLabel.setAlignment(Qt.AlignCenter)
        self.nameLabel = QLabel(title)
        self.nameLabel.setToolTip("内容：" + content)
        self.nameFont=QFont()
        #self.nameFont.setPointSize(12)
        #self.nameFont.setFamily('STKaiti')
        #self.nameFont.setBold(True)
        self.nameLabel.setFont(self.nameFont)
        self.nameLabel.setAlignment(Qt.AlignCenter)

        # 由重要性和种类得图标颜色
        self.icon = QLabel()
        iconName = str(species)
        if importance == Importance.high:
            iconName = iconName + " (1)"
        elif importance == Importance.normal:
            iconName = iconName + " (2)"
        elif importance == Importance.low:
            iconName = iconName + " (3)"
        else:
            addTask.showWarning("重要性传入有误!")

        self.icon.setPixmap(QPixmap("../Icon/taskSort2/%s.svg" % iconName).scaled(50, 50))
        self.icon.setToolTip("内容："+content)

        # 控制格式
        timeStr = "{:02d}:{:02d}".format(time.hour, time.minute)
        self.timeLabel = QLabel(timeStr)

        self.editBtn = QPushButton('编辑')

        self.switchBtn = QCheckBox('开始', self)
        self.switchBtn.toggle()
        self.deleteBtn = QPushButton()
        self.deleteBtn.setIcon(QIcon("../Icon/删除1.png"))
        self.deleteMsg = deletWindow(title)
        self.deleteBtn.clicked.connect(self.deleteMsg.show)
        self.deleteMsg.button(QMessageBox.Yes).clicked.connect(self.deleteThing)
        self.deleteBtn.setStyleSheet('''QWidget{
                                    border: none;
                                     }''')

        if self.task.getState(self.date) == State.notStarted:
            self.switchBtn.setChecked(False)
            self.switchBtn.setText('开始')
        elif self.task.getState(self.date) == State.inProgress:
            self.switchBtn.setChecked(False)
            self.switchBtn.setText('完成')
        elif self.task.getState(self.date) == State.finished:
            self.switchBtn.setChecked(True)
            self.switchBtn.setText('完成')
            self.setFinishedTasks()  # 给"已完成"的任务弄上删除线 and 变灰
        elif self.task.getState(self.date) == State.expired:
            self.switchBtn.setChecked(False)
            self.switchBtn.setText('开始')
        self.switchBtn.clicked.connect(self.switchThing)

        self.taskLayOut()
        # self.show()

    def setFinishedTasks(self):
            font = QFont()
            font.setStrikeOut(True)
            self.switchBtn.setFont(font)
            self.editBtn.setFont(font)
            self.timeLabel.setFont(font)
            self.nameLabel.setFont(font)
            self.stateLabel.setFont(font)
            self.nameLabel.setStyleSheet("QLabel{color:grey}")
            self.stateLabel.setStyleSheet("QLabel{color:grey}")
            self.timeLabel.setStyleSheet("QLabel{color:grey}")
            self.editBtn.setStyleSheet("QLabel{color:grey}")
            self.switchBtn.setStyleSheet("QLabel{color:grey}")

    def taskLayOut(self):
        self.taskGrid = QGridLayout(self)
        self.taskGrid.addWidget(self.icon, 0, 0)
        self.taskGrid.addWidget(self.stateLabel, 0, 1)
        self.taskGrid.addWidget(self.nameLabel, 0, 2)
        self.taskGrid.addWidget(self.timeLabel, 0, 3)
        self.taskGrid.addWidget(self.editBtn, 0, 4)
        self.taskGrid.addWidget(self.switchBtn, 0, 5)
        self.taskGrid.addWidget(self.deleteBtn, 0, 6)
        self.setLayout(self.taskGrid)

    def switchThing(self):
        state = self.task.getState(self.date)
        text = self.switchBtn.text()
        if state == State.notStarted:
            assert text == '开始'
            self.switchBtn.setChecked(False)
            self.switchBtn.setText('完成')
            self.user.setTaskBegin(self.task)
            self.stateLabel.setText(stateDict[self.task.getState(self.date)])
        elif state == State.inProgress:
            assert text == '完成'
            self.switchBtn.setChecked(True)
            self.finishMsg = finishWindow(self.task.title)
            self.finishMsg.show()
            self.finishMsg.button(QMessageBox.Yes).clicked.connect(self.canFinish)
            self.finishMsg.button(QMessageBox.No).clicked.connect(self.cancelFinish)
            self.stateLabel.setText(stateDict[self.task.getState(self.date)])
            self.nameLabel.setFont(self.nameFont)
            self.setFinishedTasks()  # 给"已完成"的任务弄上删除线
        elif state == State.finished:
            assert text == '完成'
            addTask.showWarning('当前待办已完成\n ' + ' \n无法重复完成待办哦')
            self.switchBtn.setChecked(True)
        else:  # 已过期的任务
            assert text == '开始'
            self.switchBtn.setChecked(False)
            if isinstance(self.task, DailyTask):
                addTask.showWarning('过期的日常待办无法开始哦')
            else:
                addTask.showWarning('当前待办已过期，可以重新编辑时间后再开始哦')

    def canFinish(self):
        # self.calenWindow.taskDisplay(None, False)
        self.user.setTaskEnd(self.task)
        self.stateLabel.setText(stateDict[self.task.getState(self.date)])

    def cancelFinish(self):
        initial = self.switchBtn.isChecked()
        # self.calenWindow.taskDisplay(None, False)
        self.switchBtn.setChecked(not initial)

    def deleteThing(self):
        self.user.deleteTask(self.task)
        self.calenWindow.taskDisplay(None, False)
        # self.calenWindow.refreshEvent()


class finishWindow(QMessageBox):
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle("确认完成操作")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setText("\n\n是否确认完成待办\n \"%s\"" % title)
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.setIconPixmap(QPixmap("../Icon/搜索无结果.svg").scaled(250, 250))
        self.sureBtn = self.button(QMessageBox.Yes)
        self.sureBtn.setText("确认")
        self.cancelBtn = self.button(QMessageBox.No)
        self.cancelBtn.setText("我再想想")


class deletWindow(QMessageBox):
    def __init__(self, title: str):
        super().__init__()
        self.setWindowTitle("确认删除操作")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setText("\n\n\n是否确认删除待办\n \"%s\"" % title)
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.setIconPixmap(QPixmap("../Icon/搜索无结果.svg").scaled(250, 250))
        self.sureBtn = self.button(QMessageBox.Yes)
        self.sureBtn.setText("确认")
        self.cancelBtn = self.button(QMessageBox.No)
        self.cancelBtn.setText("我再想想")


class DailyTaskLabel(TaskLabel):
    def __init__(self, date, task, user, calenWindow):
        super().__init__(task, user, calenWindow, date=date)
        self.editBtn.clicked.connect(self.checkState)

    def checkState(self):
        if self.task.getState(self.date) == State.expired:
            addTask.showWarning('\n该待办已过期\n不能编辑哦')
        elif self.task.getState(self.date) == State.finished:
            addTask.showWarning('\n当前待办已完成\n不能编辑哦')
        else:
            self.editDailyTaskDialog = editTask.EditDailyTaskDialog(self.user, self.calenWindow, self.task)
            self.editDailyTaskDialog.sureBtn.clicked.connect(self.editDailyTaskDialog.checkDate)
            self.editDailyTaskDialog.show()


class NormalTaskLabel(TaskLabel):
    def __init__(self, task, user, calenWindow):
        super().__init__(task, user, calenWindow)
        self.editBtn.clicked.connect(self.checkState)

    def checkState(self):
        if self.task.getState(self.date) == State.finished:
            addTask.showWarning('当前待办已完成\n不能编辑哦')
        else:
            self.editNormalTaskDialog = editTask.EditNormalTaskDialog(self.user, self.calenWindow, self.task)
            self.editNormalTaskDialog.sureBtn.clicked.connect(self.editNormalTaskDialog.checkDate)
            self.editNormalTaskDialog.show()