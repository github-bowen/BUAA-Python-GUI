import sys

from PyQt5.QtCore import QDate, QDateTime, QTime
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QApplication, QDesktopWidget, \
    QWidget, QMessageBox, QInputDialog, QMainWindow, QCalendarWidget, QFormLayout, QDateTimeEdit, QTimeEdit

from src.backend.method import *

# 星期x的对照表
from src.frontend.addTask import *

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


def checkDateExpired():
    currentDate = QDate.currentDate()
    # print("current: ", currentDate)
    selectedDate = calWindow.calendar.selectedDate()
    # print("selected: ", selectedDate)
    if currentDate > selectedDate:  # 选中日期 >= 当前日期，可添加任务
        warningForExpiredDate.show()
    else:
        selectTaskDialog.show()
        # addNormalTaskDialog.show()


if __name__ == "__main__":
    with open(".name_password.tmp", "r") as f:
        username, password = f.readlines()
    os.remove(".name_password.tmp")
    app = QApplication(sys.argv)
    calWindow = CalenWindow(username, password)

    # 添加任务设计的widget和弹窗messagebox
    addNormalTaskDialog = AddNormalTaskDialog()
    addDailyTaskDialog = AddDailyTaskDialog()
    # 在已过日期添加任务显示warning
    warningForExpiredDate = TaskAddingWarning("添加任务请求失败！\n"
                                              "不能在已经过了的日期添加任务哦！"
                                              "\n(*>﹏<*)")

    selectTaskDialog = SelectTaskDialog()  # 添加任务时的弹窗，选择日常任务还是一般任务

    calWindow.addTaskButton.clicked.connect(checkDateExpired)

    selectTaskDialog.button_dailyTask.clicked.connect(addDailyTaskDialog.show)
    addDailyTaskDialog.sureBtn.clicked.connect(addDailyTaskDialog.checkDate)

    selectTaskDialog.button_normalTask.clicked.connect(addNormalTaskDialog.show)
    addNormalTaskDialog.sureBtn.clicked.connect(addNormalTaskDialog.checkDate)

    sys.exit(app.exec_())
