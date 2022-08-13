# 星期x的对照表
from PyQt5.QtCore import QCoreApplication, Qt

from src.frontend.addTask import *
from src.frontend.qssLoader import QSSLoader
from src.frontend.timeFliter import TimeFliter
from taskDisplay import DisplayWidget
import changeStyle

weekDayLis = ['一', '二', '三', '四', '五', '六', '日']


# 主窗口（日历窗口）
class CalenWindow(QMainWindow):

    def __init__(self, username, password):
        super().__init__()

        changeStyle.run(self, "calendar", 700, 400)

        self.user = loginUser(username, password)
        self.initUI()

    def initUI(self):
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

        displayWidget = DisplayWidget(self.user)  # 获取滚动条

        displayWidget.layout = QVBoxLayout(displayWidget)
        displayWidget.layout.addWidget(displayWidget.scroll)

        grid = QGridLayout(self)
        grid.setSpacing(20)
        # 点击某个日期时使其在下方显示具体年月日
        self.calendar = QCalendarWidget(self)
        self.setMinimumSize(800, 500)  # todo: 这么改大小感觉怪怪的
        self.setFixedSize(800, 500)
        self.calendar.setGridVisible(True)
        self.calendar.clicked[QDate].connect(self.dateDisplay)
        self.dateLabel = QLabel(self)
        date = self.calendar.selectedDate()
        self.dateLabel.setText(self.dateToStr(date))

        # 设置控件的栅格布局
        grid.addWidget(self.calendar, 0, 0, 3, 3)
        grid.addWidget(self.dateLabel, 3, 0, 1, 3)
        grid.addLayout(displayWidget.layout, 0, 3, 3, 1)

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
        icon.addPixmap(QtGui.QPixmap("../Icon/新建方案.png"))
        self.addNewTask.setIcon(icon)
        self.addNewTask.setObjectName("addNewTask")
        self.fliterTask = QtWidgets.QAction(self)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../Icon/筛选.png"))
        self.fliterTask.setIcon(icon1)
        self.fliterTask.setObjectName("fliterTask")
        self.refreshTask = QtWidgets.QAction(self)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../Icon/刷新.png"))
        self.refreshTask.setIcon(icon2)
        self.refreshTask.setObjectName("refreshTask")
        self.dispatchTask = QtWidgets.QAction(self)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../Icon/调度.png"))
        self.dispatchTask.setIcon(icon3)
        self.dispatchTask.setObjectName("dispatchTask")
        self.toolBar.addAction(self.addNewTask)
        self.toolBar.addAction(self.fliterTask)
        self.toolBar.addAction(self.refreshTask)
        self.toolBar.addAction(self.dispatchTask)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))
        self.toolBar.setWindowTitle(_translate("self", "toolBar"))
        self.addNewTask.setText(_translate("self", "添加新待办"))
        self.addNewTask.setToolTip(_translate("self", "点击添加新的待办事项"))
        self.addNewTask.setShortcut(_translate("self", "Ctrl+N"))
        self.fliterTask.setText(_translate("self", "筛选"))
        self.fliterTask.setToolTip(_translate("self", "点击按时间过滤任务"))
        self.fliterTask.setShortcut(_translate("self", "Ctrl+Shift+L"))
        self.refreshTask.setText(_translate("self", "刷新"))
        self.refreshTask.setToolTip(_translate("self", "点击刷新任务列表"))
        self.refreshTask.setShortcut(_translate("self", "F5"))
        self.dispatchTask.setText(_translate("self", "调度任务列表"))
        self.dispatchTask.setToolTip(_translate("self", "点击调度未来任务列表"))
        self.dispatchTask.setShortcut(_translate("self", "Ctrl+D"))

    # TODO：所有回到日历主页面的按钮都应触发该函数，考虑引入缓存
    def taskDisplay(self, date):
        taskLis = self.user.getTasksOfDay(date)

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

    '''
    样式表的设置模板:
    styleFile = './style.qss'
    styleSheet = QSSLoader.readFile(styleFile)
    calWindow.setStyleSheet(styleSheet)
    '''

    # 添加任务设计的widget和弹窗messagebox
    addNormalTaskDialog = AddNormalTaskDialog(username, password)
    addDailyTaskDialog = AddDailyTaskDialog(username, password)
    # 在已过日期添加任务显示warning
    warningForExpiredDate = TaskAddingWarning("添加任务请求失败！\n"
                                              "不能在已经过了的日期添加任务哦！"
                                              "\n(*>﹏<*)")

    selectTaskDialog = SelectTaskDialog()  # 添加任务时的弹窗，选择日常任务还是一般任务

    calWindow.addNewTask.triggered.connect(checkDateExpired)

    selectTaskDialog.button_dailyTask.clicked.connect(addDailyTaskDialog.show)
    addDailyTaskDialog.sureBtn.clicked.connect(addDailyTaskDialog.checkDate)

    selectTaskDialog.button_normalTask.clicked.connect(addNormalTaskDialog.show)
    addNormalTaskDialog.sureBtn.clicked.connect(addNormalTaskDialog.checkDate)

    # 筛选任务的界面
    timeFliter=TimeFliter(username, password)
    calWindow.fliterTask.triggered.connect(timeFliter.show)

    sys.exit(app.exec_())
