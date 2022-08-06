import sys

from PyQt5.QtCore import QDate
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import qApp, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QApplication, QDesktopWidget, \
    QWidget, QMessageBox, QInputDialog, QMainWindow, QCalendarWidget, QFormLayout, QDateTimeEdit

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

    def addTask(self):
        pass


# 添加任务的子窗口
class AddTaskDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        dialogGrid = QGridLayout()
        self.titleLbl = QLabel('待办名称：')
        self.titleLE = QLineEdit()

        self.beginTimeLbl = QLabel('起始时间：')
        self.beginTimeLE = QDateTimeEdit()
        self.endTimeLbl = QLabel('截止时间：')
        self.endTimeLE = QDateTimeEdit()

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
        self.setWindowTitle('创建新的待办')

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


if __name__ == "__main__":
    with open(".name_password.tmp", "r") as f:
        username, password = f.readlines()
    os.remove(".name_password.tmp")
    app = QApplication(sys.argv)
    calWindow = CalenWindow(username, password)
    addTaskDialog = AddTaskDialog()
    calWindow.addTaskButton.clicked.connect(addTaskDialog.show)
    addTaskDialog.sureBtn.clicked.connect(calWindow.addTask)
    sys.exit(app.exec_())
