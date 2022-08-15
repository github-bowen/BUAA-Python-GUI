import datetime

from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QScrollArea, QVBoxLayout, \
    QGroupBox, QLabel, QFormLayout, QFrame, QSizePolicy, QHBoxLayout

from TaskLabel import NormalTaskLabel, DailyTaskLabel
from src.backend.Module import DailyTask


class DisplayWidget(QWidget):
    def __init__(self, user, calenWindow, dateToDisplay):
        super().__init__()
        self.calenWindow = calenWindow
        self.taskNum = 0
        self.formLayout = QFormLayout()
        self.groupBox = QGroupBox()
        self.user = user
        self.allTasks = None
        self.displayingDate = dateToDisplay

        self.displayingTasks = self.getTaskOfDate(dateToDisplay)
        self.taskNum = len(self.displayingTasks)

        if self.taskNum > 0:
            widget = QLabel("所选日期待办如下：")
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
            sortLabel = QLabel('   类别')
            stateLabel = QLabel('   状态')
            nameLabel = QLabel('    名称')
            timeLabel = QLabel('    时间')
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
            self.displayNoTaskToday()

        self.scroll = QScrollArea()
        self.disableHorizontalScroll()
        self.scroll.setWidget(self.groupBox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(400)  # 对应CalenWindow高度
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll)
        # self.show()

    def disableHorizontalScroll(self):
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameStyle(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.m_scrollAreaWidgetContents = QWidget(self)
        self.m_scrollAreaWidgetContents.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        baseLayout = QVBoxLayout(self.m_scrollAreaWidgetContents)
        self.scroll.setWidget(self.m_scrollAreaWidgetContents)
        self.m_scrollAreaWidgetContents.installEventFilter(self)

    def eventFilter(self, o: QObject, e: QEvent) -> bool:
        if o == self.m_scrollAreaWidgetContents and e.type() == QEvent.Resize:
            self.scroll.setMinimumWidth(
                self.m_scrollAreaWidgetContents.minimumSizeHint().width() +
                self.scroll.verticalScrollBar().width())

        return super(DisplayWidget, self).eventFilter(o, e)

    @staticmethod
    def clearLayout(layout):
        item_list = list(range(layout.count()))
        item_list.reverse()  # 倒序删除，避免影响布局顺序
        for i in item_list:
            item = layout.itemAt(i)
            layout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()

    def refreshAndDisplay(self, date, dateChanged: bool):
        # DisplayWidget.clearLayout(self.formLayout)
        #print(0)

        if dateChanged:
            # print(date.__class__)
            #print(1)
            dtdt = datetime.datetime(date.year(), date.month(), date.day(), 0, 0, 0)
            self.displayingDate = dtdt
            self.displayingTasks = self.getTaskOfDate(dtdt)
        else:
            self.displayingTasks = self.getTaskOfDate(self.displayingDate)
        self.taskNum = len(self.displayingTasks)

        #print(2)
        if self.taskNum > 0:
            widget = QLabel("所选日期待办如下：")
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
            sortLabel = QLabel('   类别')
            stateLabel = QLabel('   状态')
            nameLabel = QLabel('    名称')
            timeLabel = QLabel('    时间')
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

            #print(3)
            for task in self.displayingTasks:
                widget = self.generateTaskWidget(task)
                self.formLayout.addRow(widget)
            # self.groupBox.setLayout(self.formLayout)
        else:
            self.displayNoTaskToday(False)

        #print(4)
        self.groupBox.repaint()
        self.scroll.repaint()
        self.repaint()

    def displayNoTaskToday(self, first=True):  # 显示下面的提示文字
        label = QLabel("所选日期暂无待办哦～")
        label.setStyleSheet("QLabel{color:#015F17}")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        # font.setFamily("KaiTi")
        label.setFont(font)
        tipLabel = QLabel("可通过上方工具栏添加待办")
        tipLabel.setStyleSheet("QLabel{color:#015F17}")
        font.setPointSize(14)
        font.setBold(False)
        tipLabel.setFont(font)
        tipLabel2=QLabel('          或使用快捷键Ctrl+N创建新代办')
        tipLabel2.setFont(font)
        tipLabel2.setStyleSheet("QLabel{color:#015F17}")

        self.formLayout.addWidget(label)
        self.formLayout.addWidget(QLabel())
        self.formLayout.addWidget(tipLabel)
        self.formLayout.addWidget(QLabel())
        self.formLayout.addWidget(tipLabel2)
        if first:
            self.groupBox.setLayout(self.formLayout)

    def getTodayTask(self) -> list:
        return self.user.getTaskToday()

    def generateTaskWidget(self, task):
        if isinstance(task, DailyTask):
            taskLabel = DailyTaskLabel(date=self.displayingDate, task=task, user=self.user,
                                       calenWindow=self.calenWindow)
        else:
            taskLabel = NormalTaskLabel(task=task, user=self.user, calenWindow=self.calenWindow)
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
