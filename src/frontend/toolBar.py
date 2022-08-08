# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toolBar.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.addNewTask = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../Icon/新建方案.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addNewTask.setIcon(icon)
        self.addNewTask.setObjectName("addNewTask")
        self.fliterTask = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../Icon/筛选.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fliterTask.setIcon(icon1)
        self.fliterTask.setObjectName("fliterTask")
        self.refreshTask = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../../Icon/刷新.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshTask.setIcon(icon2)
        self.refreshTask.setObjectName("refreshTask")
        self.dispatchTask = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../../Icon/调度.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.dispatchTask.setIcon(icon3)
        self.dispatchTask.setObjectName("dispatchTask")
        self.toolBar.addAction(self.addNewTask)
        self.toolBar.addAction(self.fliterTask)
        self.toolBar.addAction(self.refreshTask)
        self.toolBar.addAction(self.dispatchTask)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.addNewTask.setText(_translate("MainWindow", "添加新代办"))
        self.addNewTask.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">点击添加新的待办事项</span></p></body></html>"))
        self.addNewTask.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.fliterTask.setText(_translate("MainWindow", "筛选"))
        self.fliterTask.setToolTip(_translate("MainWindow", "点击按时间过滤任务"))
        self.fliterTask.setShortcut(_translate("MainWindow", "Ctrl+Shift+L"))
        self.refreshTask.setText(_translate("MainWindow", "刷新"))
        self.refreshTask.setToolTip(_translate("MainWindow", "点击刷新任务列表"))
        self.refreshTask.setShortcut(_translate("MainWindow", "F5"))
        self.dispatchTask.setText(_translate("MainWindow", "调度任务列表"))
        self.dispatchTask.setToolTip(_translate("MainWindow", "点击自动调度任务"))
        self.dispatchTask.setShortcut(_translate("MainWindow", "Ctrl+D"))
