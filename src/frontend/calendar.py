import sys

from PyQt5.QtCore import QDate, QDateTime, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QApplication, QDesktopWidget, \
    QWidget, QMessageBox, QInputDialog, QMainWindow, QCalendarWidget, QFormLayout, QDateTimeEdit, QTimeEdit

from src.backend.method import *

# 星期x的对照表
weekDayLis = ['一', '二', '三', '四', '五', '六', '日']


# 主窗口（日历窗口）
class CalenWindow(QMainWindow):

    def __init__(self, username, password):
        super().__init__()

        self.user = loginUser(username, password)
        self.initUI()

    def initUI(self):
        grid = QGridLayout(self)
        grid.setSpacing(5)
        # 点击某个日期时使其在下方显示具体年月日
        self.calendar = QCalendarWidget(self)
        self.setMinimumSize(600, 400)  # todo: 这么改大小感觉怪怪的
        self.calendar.setGridVisible(True)
        self.calendar.clicked[QDate].connect(self.dateDisplay)
        self.dateLabel = QLabel(self)
        date = self.calendar.selectedDate()
        self.dateLabel.setText(self.dateToStr(date))

        # 管理任务的添加，放到了主函数中，唤醒子窗口
        self.addTaskButton = QPushButton(QIcon('hh.jpg'), '点击此处添加任务')

        # 设置控件的栅格布局
        grid.addWidget(self.calendar, 0, 0)
        grid.addWidget(self.dateLabel, 1, 0)
        grid.addWidget(self.addTaskButton, 0, 1)

        # 由父类为QMainWindow
        tempWidget = QWidget()
        tempWidget.setLayout(grid)
        self.setCentralWidget(tempWidget)
        self.show()

    def dateToStr(self, date):
        return \
            '这一天是 ' + str(date.year()) + ' 年 ' \
            + str(date.month()) + ' 月 ' \
            + str(date.day()) + ' 日 ' \
            + '星期' + weekDayLis[date.dayOfWeek() - 1]

    def dateDisplay(self, date):
        self.dateLabel.setText(self.dateToStr(date))

    def addDailyTask(self):
        pass

    def addNormalTask(self):
        pass


def checkDateExpired():
    currentDate = QDate.currentDate()
    # print("current: ", currentDate)
    selectedDate = calWindow.calendar.selectedDate()
    # print("selected: ", selectedDate)
    if currentDate > selectedDate:  # 选中日期 >= 当前日期，可添加任务
        taskAddingWarning.show()
    else:
        selectTaskDialog.show()
        # addNormalTaskDialog.show()


class SelectTaskDialog(QMessageBox):  # 选择添加"日常任务"还是"一般任务"
    def __init__(self):
        super().__init__()
        self.setIcon(QMessageBox.Information)
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


class TaskAddingWarning(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setText("添加任务请求失败！\n不能在已经过了的日期添加任务哦！\n(*>﹏<*)")
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle("提示")
        self.setStandardButtons(QMessageBox.Yes)
        button = self.button(QMessageBox.Yes)
        button.setText("确定")


if __name__ == "__main__":
    with open(".name_password.tmp", "r") as f:
        username, password = f.readlines()
    os.remove(".name_password.tmp")
    app = QApplication(sys.argv)
    calWindow = CalenWindow(username, password)

    # 添加任务设计的widget和弹窗messagebox
    addNormalTaskDialog = AddNormalTaskDialog()
    addDailyTaskDialog = AddDailyTaskDialog()
    taskAddingWarning = TaskAddingWarning()  # 在已过日期添加任务显示warning
    selectTaskDialog = SelectTaskDialog()  # 添加任务时的弹窗，选择日常任务还是一般任务

    calWindow.addTaskButton.clicked.connect(checkDateExpired)

    selectTaskDialog.button_dailyTask.clicked.connect(addDailyTaskDialog.show)
    addDailyTaskDialog.sureBtn.clicked.connect(calWindow.addDailyTask)

    selectTaskDialog.button_normalTask.clicked.connect(addNormalTaskDialog.show)
    addNormalTaskDialog.sureBtn.clicked.connect(calWindow.addNormalTask)

    sys.exit(app.exec_())
