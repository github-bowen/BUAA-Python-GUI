'''
    def addDailyTask(self):
        name, time, content, importance,species = self.titleLE.text() \
            , self.beginTimeLE.time(), self.endTimeLE.time(), self.importanceBtn.text()\
            ,self.sortLE.text()
        self.user.addTask(name,content,end)
'''
import sys
from datetime import datetime

from PyQt5.QtCore import pyqtSignal

from src.backend.Module import Task
from src.backend.importance import *
import addTask
import editTask

from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout, \
    QApplication, QWidget, QCheckBox, QMessageBox

from src.backend.species import Species

class taskLabel(QWidget):
    def __init__(self,task:Task):
        super().__init__()
        self.initUi(task)

    def initUi(self,task:Task):
        title=task.title
        importance=task.importance
        species=task.species
        time=task.time
        self.nameLabel=QLabel(title)

        #由重要性和种类得图标颜色
        self.icon=QLabel()
        iconName = str(species)
        if importance==Importance.high:
            iconName= iconName+" (2)"
        elif importance==Importance.normal:
            iconName= iconName+" (3)"
        elif importance==Importance.low:
            iconName= iconName+" (1)"
        else:
            addTask.showWarning("重要性传入有误!")
        self.icon.setPixmap(QPixmap("../Icon/taskSort/%s.png"%iconName).scaled(50,50))

        # 控制格式
        timeStr="{:02d}:{:02d}".format(time.hour,time.minute)
        self.timeLabel=QLabel(timeStr)

        self.editBtn=QPushButton('编辑')

        # 开始只有按下和弹起两种状态
        self.beginBtn=QPushButton('开始')
        self.beginBtn.setCheckable(True)
        self.beginBtn.clicked[bool].connect(self.beginThing)

        self.finshBtn = QCheckBox('完成', self)
        self.finshBtn.toggle()
        self.finshBtn.setChecked(False)
        self.finshBtn.stateChanged.connect(self.finshThing)

        '''
        下为按钮模式
        self.finshBtn=QPushButton('完成')
        self.finshBtn.clicked.connect(self.finshThing)
        '''
        self.deleteBtn=QPushButton()
        self.deleteBtn.setIcon(QIcon("../Icon/删除.png"))
        self.deleteMsg=deletWindow(title)
        self.deleteBtn.clicked.connect(self.deleteMsg.show)
        self.deleteMsg.button(QMessageBox.Yes).clicked.connect(self.deleteThing)

        self.taskLayOut()
        self.show()

    def taskLayOut(self):
        self.taskGrid=QGridLayout(self)
        self.taskGrid.addWidget(self.icon, 0, 0)
        self.taskGrid.addWidget(self.nameLabel, 0, 1)
        self.taskGrid.addWidget(self.timeLabel, 0, 2)
        self.taskGrid.addWidget(self.editBtn, 0, 3)
        self.taskGrid.addWidget(self.beginBtn,0,4)
        self.taskGrid.addWidget(self.finshBtn, 0, 5)
        self.taskGrid.addWidget(self.deleteBtn,0,6)
        self.setLayout(self.taskGrid)


    def beginThing(self):
        pass

    def finshThing(self):
        #TODO：将事件设置为完成状态，同时触发calenderFront的taskDisplay函数
        # 如果还没选中开始按钮就已经按了结束
        if not self.beginBtn.isChecked():
            addTask.showWarning("\n 当前任务尚未开始\n 无法完成哦")
            self.finshBtn.setChecked(False)
        else:
            pass

    def deleteThing(self):
        pass



class deletWindow(QMessageBox):
    def __init__(self,title:str):
        super().__init__()
        self.setWindowTitle("确认删除操作")
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.setText("确认删除待办\n \"%s\" 吗？"%title)
        self.setIconPixmap(QPixmap("../Icon/记录.png").scaled(250, 250))
        self.sureBtn=self.button(QMessageBox.Yes)
        self.sureBtn.setText("确认")
        self.cancelBtn=self.button(QMessageBox.No)
        self.cancelBtn.setText("我再想想")


class dailyTaskLabel(taskLabel):
    def __init__(self, username, password, task: Task):
        super().__init__(task)
        self.editDailyTaskDialog = editTask.EditDailyTaskDialog(username, password, task)
        self.editDailyTaskDialog.sureBtn.clicked.connect(self.editDailyTaskDialog.checkDate)
        self.editBtn.clicked.connect(self.editDailyTaskDialog.show)


class normalTaskLabel(taskLabel):
    def __init__(self,username,password,task:Task):
        super().__init__(task)
        self.editNormalTaskDialog= editTask.EditNormalTaskDialog(username, password, task)
        self.editBtn.clicked.connct(self.editNormalTaskDialog.show)
        self.editNormalTaskDialog.sureBtn.clicked.connect(self.editNormalTaskDialog.checkDate)

# 测试
if __name__=="__main__":
    app = QApplication(sys.argv)
    date=datetime.now()
    task=Task('检查','',date,importance=Importance.normal,speices=Species.sport)
    text=dailyTaskLabel('匡莉','zjtdbd',task)
    app.exec_()



