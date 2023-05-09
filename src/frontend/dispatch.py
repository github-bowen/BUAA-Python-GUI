# 点击工具栏的调度按钮所显示的页面
from src.backend.method import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFormLayout, \
    QGroupBox, QScrollArea, QFrame

from src.frontend.TaskLabel import DailyTaskLabel, NormalTaskLabel


class Dispatcher(QWidget):
    def __init__(self, user, calenWindow):
        super(Dispatcher, self).__init__()
        # self.width(),self.height()=800,800
        # changeStyle.run(self, "dispatch", 800,450)
        self.scroll = QScrollArea()
        self.user = user
        self.calenWindow = calenWindow
        self.displayingTasks = None
        self.initUI()

    def initUI(self):
        self.formLayout = QFormLayout()
        self.groupBox = QGroupBox()
        '''
        self.backgroundLabel=QLabel()
        self.backgroundLabel.setPixmap(QPixmap("../Icon/工作安排.png"))
        self.backgroundLabel.autoFillBackground()
        '''

        self.displayingTasks = self.user.scheduleTasks()
        self.taskNum = len(self.displayingTasks)

        if self.taskNum > 0:
            widget = QLabel("今日所有待办的调度安排如下：")
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
            sortLabel = QLabel('类别')
            stateLabel = QLabel('状态')
            nameLabel = QLabel('名称')
            timeLabel = QLabel('时间')
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
            label = QLabel("今日暂无可执行的待办\n\t\t不需要进行调度哦～")
            font = QFont()
            font.setPointSize(16)
            font.setBold(True)
            # font.setFamily("KaiTi")
            label.setFont(font)

            self.formLayout.addWidget(label)
            self.formLayout.addWidget(QLabel())
            self.groupBox.setLayout(self.formLayout)

        # self.disableHorizontalScroll()
        self.scroll.setWidget(self.groupBox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(400)  # 对应CalenWindow高度
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll)

        self.disableHorizontalScroll()
        # self.show()

    def generateTaskWidget(self, task: Task):
        if isinstance(task, DailyTask):
            taskLabel = DailyTaskLabel(date=task.time, task=task, user=self.user,
                                       calenWindow=self.calenWindow)
        else:
            taskLabel = NormalTaskLabel(task=task, user=self.user, calenWindow=self.calenWindow)
        return taskLabel

    def disableHorizontalScroll(self):
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameStyle(QFrame.NoFrame)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        """
        self.m_scrollAreaWidgetContents = QWidget(self)
        self.m_scrollAreaWidgetContents.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        baseLayout = QVBoxLayout(self.m_scrollAreaWidgetContents)
        self.scroll.setWidget(self.m_scrollAreaWidgetContents)
        self.m_scrollAreaWidgetContents.installEventFilter(self)
        """
