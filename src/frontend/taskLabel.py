'''
    def addDailyTask(self):
        name, time, content, importance,species = self.titleLE.text() \
            , self.beginTimeLE.time(), self.endTimeLE.time(), self.importanceBtn.text()\
            ,self.sortLE.text()
        self.user.addTask(name,content,end)
'''
from datetime import datetime
from src.backend.importance import *

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import qApp, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QApplication, QDesktopWidget, \
    QWidget, QMessageBox, QInputDialog, QCheckBox
class taskLabel(QWidget):
    def __init__(self,title:str,importance:int,species:str,time:datetime):
        super().__init__()
        self.initUi(title,importance,species,time)


    def initUi(self,title:str,importance:int,species:str,time:datetime):
        self.nameLabel=QLabel(title)
        self.icon=QIcon()
        if importance==Importance.high:
            iconName="high"
        elif importance==Importance.normal:
            iconName='normal'
        else:
            iconName='low'
        iconName=iconName+'_'+species
        self.icon.addPixmap(QPixmap("../Icon/%s.png"%iconName))
        self.timeLabel=QLabel(datetime.time)
        self.editBtn=QPushButton('编辑')
        self.editBtn.clicked.connect(self.editThing)
        self.beginBtn=QPushButton('开始')
        self.beginBtn.clicked.connect(self.beginThing)
        self.finshBtn=QPushButton('完成')
        self.finshBtn.clicked.connect(self.finshThing)

    def taskLayOut(self):
        pass

    def editThing(self):
        pass

    def beginThing(self):
        pass

    def finshThing(self):
        pass





