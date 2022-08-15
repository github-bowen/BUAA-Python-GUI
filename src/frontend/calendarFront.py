import sys

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QCalendarWidget, QLabel, QApplication

from src.backend.method import loginUser
from src.frontend.addTask import TaskAddingWarning, SelectTaskDialog
from src.frontend.dispatch import Dispatcher
from src.frontend.timeFilter import TimeFilter
from analyze import *
from taskDisplay import DisplayWidget
import changeStyle

# 星期x的对照表
weekDayLis = ['一', '二', '三', '四', '五', '六', '日']


# 主窗口（日历窗口）
class CalenWindow(QMainWindow):

    def __init__(self, username, password):
        super().__init__()

        self.width, self.height = 1000, 500
        changeStyle.run(self, "calendar", self.width, self.height)

        self.user = loginUser(username, password)
        self.initUI()

    def initUI(self):
        # QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

        self.displayWidget = DisplayWidget(self.user, self, dateToDisplay)  # 获取滚动条
        self.displayWidget.layout = QVBoxLayout(self.displayWidget)
        self.displayWidget.layout.addWidget(self.displayWidget.scroll)

        grid = QGridLayout(self)
        grid.setSpacing(20)
        # 点击某个日期时使其在下方显示具体年月日
        self.calendar = QCalendarWidget(self)
        self.setMinimumSize(self.width, self.height)  # todo: 这么改大小感觉怪怪的
        self.setFixedSize(self.width, self.height)
        self.calendar.setGridVisible(True)
        self.calendar.clicked[QDate].connect(self.dateDisplay)
        # https://jingyan.baidu.com/article/b907e6270f080906e6891c65.html
        self.calendar.setStyleSheet('''QWidget{
                            color: black;
                            background-color: white;
                            selection-color: white;
                            selection-background-color: #4CAF50;
                            alternate-background-color: #C8E6C9;
                             }''')
        qtcf = QtGui.QTextCharFormat()
        qtcf.setForeground(QtGui.QColor("#015F17"))
        # qtcf.setBackground(QtGui.QColor("#BDBDBD"))
        self.calendar.setWeekdayTextFormat(Qt.Saturday, qtcf)
        self.calendar.setWeekdayTextFormat(Qt.Sunday, qtcf)
        self.dateLabel = QLabel(self)
        date = self.calendar.selectedDate()
        self.dateLabel.setText(self.dateToStr(date))

        # 设置控件的栅格布局
        grid.addWidget(self.calendar, 0, 0, 3, 3)
        grid.addWidget(self.dateLabel, 3, 0, 1, 3)
        grid.addLayout(self.displayWidget.layout, 0, 3, 3, 1)

        # 由父类为QMainWindow
        tempWidget = QWidget()
        tempWidget.setLayout(grid)
        self.initToolBar()
        self.setCentralWidget(tempWidget)
        self.show()

    def initToolBar(self):
        self.toolBar = QtWidgets.QToolBar(self)
        self.toolBar.setObjectName("toolBar")
        self.addToolBar(self.toolBar)

        # 管理任务的添加，放到了主函数中，唤醒子窗口
        self.addNewTask = QtWidgets.QAction(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Icon/icon2/新建方案.svg"))
        self.addNewTask.setIcon(icon)
        self.addNewTask.setObjectName("addNewTask")
        self.filterTask = QtWidgets.QAction(self)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../Icon/icon2/筛选.svg"))
        self.filterTask.setIcon(icon1)
        self.filterTask.setObjectName("fliterTask")
        self.refreshTask = QtWidgets.QAction(self)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../Icon/icon2/刷新.svg"))
        self.refreshTask.setIcon(icon2)
        self.refreshTask.setObjectName("refreshTask")
        self.dispatchTask = QtWidgets.QAction(self)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../Icon/icon2/调度.svg"))
        self.dispatchTask.setIcon(icon3)
        self.dispatchTask.setObjectName("dispatchTask")


        self.analyzeTask = QtWidgets.QAction(self)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../Icon/icon2/统计.svg"))
        self.analyzeTask.setIcon(icon4)
        self.analyzeTask.setObjectName("analyzeTask")

        self.toolBar.addAction(self.addNewTask)
        self.toolBar.addAction(self.filterTask)
        self.toolBar.addAction(self.refreshTask)
        self.toolBar.addAction(self.dispatchTask)
        self.toolBar.addAction(self.analyzeTask)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "任务管理器-主页面"))
        self.toolBar.setWindowTitle(_translate("self", "工具栏"))
        self.addNewTask.setText(_translate("self", "添加新待办"))
        self.addNewTask.setToolTip(_translate("self", "点击添加新的待办事项"))
        self.addNewTask.setShortcut(_translate("self", "Ctrl+N"))
        self.filterTask.setText(_translate("self", "筛选"))
        self.filterTask.setToolTip(_translate("self", "点击按时间过滤任务"))
        self.filterTask.setShortcut(_translate("self", "Ctrl+Shift+L"))
        self.refreshTask.setText(_translate("self", "刷新"))
        self.refreshTask.setToolTip(_translate("self", "点击刷新任务列表"))
        self.refreshTask.setShortcut(_translate("self", "F5"))
        self.dispatchTask.setText(_translate("self", "调度任务列表"))
        self.dispatchTask.setToolTip(_translate("self", "点击调度未来任务列表"))
        self.dispatchTask.setShortcut(_translate("self", "Ctrl+D"))

    # 所有回到日历主页面的按钮都应触发该函数，考虑引入缓存
    # TODO: 记录下要显示的date，然后销毁当前日历对象，重新new一个
    def taskDisplay(self, date, dateChange: bool):
        """
        global dateToDisplay, closeBecauseOfRefresh
        if dateChange:
            dtdt = datetime.datetime(date.year(), date.month(), date.day())
            dateToDisplay = dtdt
        else:
            dateToDisplay = self.displayWidget.displayingDate
        closeBecauseOfRefresh = True
        # print(date)  # debug用
        qApp.exit()
        """
        # self.displayWidget.close()
        # self.displayWidget = DisplayWidget(self.user, self)
        # self.displayWidget.refreshAndDisplay(date=date, dateChanged=dateChange)
        fl = self.displayWidget.formLayout
        for i in range(len(fl)):
            fl.removeRow(0)
        #print("before refresh")
        self.displayWidget.refreshAndDisplay(date, dateChange)
        pass

    def refreshEvent(self):  # 点击刷新后触发执行的方法
        self.taskDisplay(None, False)

    def dispatch(self):
        #print("333333333")
        self.dispatcher = Dispatcher(user=calWindow.user, calenWindow=calWindow)
        #print("222222222")
        self.dispatcher.layout = QVBoxLayout(self.dispatcher)
        self.dispatcher.layout.addWidget(self.dispatcher.scroll)
        self.tempWidget = QWidget()
        self.tempWidget.setLayout(self.dispatcher.layout)
        #print("111111111")
        self.tempWidget.setWindowTitle("每日任务自动调度")
        self.tempWidget.show()

    def dateToStr(self, date):
        return \
            '这一天是 ' + str(date.year()) + ' 年 ' \
            + str(date.month()) + ' 月 ' \
            + str(date.day()) + ' 日 ' \
            + '星期' + weekDayLis[date.dayOfWeek() - 1]

    def dateDisplay(self, date):
        self.dateLabel.setText(self.dateToStr(date))
        self.taskDisplay(date, True)


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
    #
    # with open(".name_password.tmp", "r") as f:
    #     username, password = f.readlines()
    # os.remove(".name_password.tmp")

    username, password = "test", "test1234"

    app = QApplication(sys.argv)

    first = True  # 第一次打开程序
    dateToDisplay = None  # 下一次要显示任务的日期
    closeBecauseOfRefresh = True  # 记录窗口关闭是否是因为进行了refresh
    while closeBecauseOfRefresh:

        closeBecauseOfRefresh = False
        if first:
            first = False
            dateToDisplay = datetime.datetime.today()
            print(dateToDisplay)

        calWindow = CalenWindow(username, password)

        '''
        样式表的设置模板:
        styleFile = './style.qss'
        styleSheet = QSSLoader.readFile(styleFile)
        calWindow.setStyleSheet(styleSheet)
        '''


        # 在已过日期添加任务显示warning
        warningForExpiredDate = TaskAddingWarning("添加任务请求失败！\n"
                                                  "不能在已经过了的日期添加任务哦！"
                                                  "\n(*>﹏<*)")

        selectTaskDialog = SelectTaskDialog(calWindow)  # 添加任务时的弹窗，选择日常任务还是一般任务

        calWindow.addNewTask.triggered.connect(checkDateExpired)


        # 筛选任务的界面
        timeFilter = TimeFilter(user=calWindow.user, calenWindow=calWindow)
        calWindow.filterTask.triggered.connect(timeFilter.show)

        # 刷新任务
        calWindow.refreshTask.triggered.connect(calWindow.refreshEvent)

        # 调度任务的界面
        calWindow.dispatchTask.triggered.connect(calWindow.dispatch)

        analyze = AnalyzeWindow(calWindow.user)
        calWindow.analyzeTask.triggered.connect(analyze.refresh)

        app.exec_()
        app.closeAllWindows()
        calWindow.close()
        del calWindow

    exit(0)
