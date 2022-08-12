import sys

from src.backend.method import *
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import QDate, QDateTime, QTime
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtWidgets import qApp, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QApplication, QDesktopWidget, \
    QWidget, QMessageBox, QInputDialog, QMainWindow, QCalendarWidget, QFormLayout, QDateTimeEdit, QTimeEdit, QTextEdit

class TimeFliter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.timeFliterLayOut()
        self.show()

    def initUi(self):
        self.titleLbl = QLabel('筛选相应时间段的任务')
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setFamily("KaiTi")
        self.titleLbl.setFont(font)
        self.beginLbl=QLabel('请选取起始时间:')
        self.beginIcon = QLabel()
        self.beginIcon.setPixmap(QPixmap("../Icon/时间.png").scaled(50, 40))
        self.beginTE=QDateTimeEdit()
        self.beginTE.setDateTime(QDateTime.currentDateTime())
        self.endLbl = QLabel('请选取截止时间:')
        self.endIcon = QLabel()
        self.endIcon.setPixmap(QPixmap("../Icon/时间 (1).png").scaled(50, 40))
        self.endTE = QDateTimeEdit()
        self.endTE.setDateTime(QDateTime.currentDateTime())

    def timeFliterLayOut(self):
        self.grid=QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.titleLbl, 0, 0, 2, 1)
        self.form=QFormLayout()
        self.form.addRow(self.beginIcon, self.beginLbl)
        self.form.addRow(self.beginTE)
        self.form.addRow(self.endIcon, self.endLbl)
        self.form.addRow(self.endTE)
        self.grid.addLayout(self.form,4,0)
        self.setLayout(self.grid)


if __name__=="__main__":
    app = QApplication(sys.argv)
    timeFliter=TimeFliter()
    app.exec_()
