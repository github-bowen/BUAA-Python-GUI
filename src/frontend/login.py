import sys

from PyQt5.QtWidgets import qApp, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QApplication, QDesktopWidget, \
    QWidget, QMessageBox, QInputDialog

from src.backend.method import *


class LoginWindow(QWidget):
    def __init__(self):
        # 创建标题文字
        self.title = QLabel('欢迎使用任务调度管理系统！')

        # 创建标签、文本框、按钮
        self.usernameLabel = QLabel('用户名：')
        self.passwordLabel = QLabel('密码：')

        self.usernameEdit = QLineEdit()
        self.passwordEdit = QLineEdit()

        self.loginButton = QPushButton('登录')
        self.registerButton = QPushButton('注册')

        # 以__开头的变量或函数为个人内部或临时的变量或函数，不用在意！！！
        self.__messageBoxForUsername = None
        self.__button_inputAgain = None
        self.__button_exit = None
        self.__formerPassword = None

        super().__init__()
        self.initUI()

    def initUI(self):
        # 布局用户名和密码的label和输入框
        grid = QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(self.title, 0, 1, 3, 2)
        grid.addWidget(self.usernameLabel, 3, 0)
        grid.addWidget(self.usernameEdit, 3, 1, 1, 3)
        grid.addWidget(self.passwordLabel, 4, 0)
        grid.addWidget(self.passwordEdit, 4, 1, 1, 3)

        # 布局登录和注册按钮
        hBox = QHBoxLayout()
        hBox.addStretch(1)
        hBox.addWidget(self.loginButton)
        hBox.addWidget(self.registerButton)

        vBox = QVBoxLayout()
        vBox.addStretch(1)
        vBox.addLayout(hBox)

        # 设置事件
        # 设置"登录"Button点击后的事件
        self.loginButton.clicked.connect(self.checkLoginButton)
        # 设置"注册"Button点击后的事件
        self.registerButton.clicked.connect(self.checkRegisterButton)

        # 布局整个窗口
        grid.addLayout(vBox, 6, 2)
        self.setLayout(grid)
        self.resize(300, 150)
        self.center()
        self.setWindowTitle("任务调度器-登录")
        self.show()

    def center(self):  # 让当前窗口居中，该部分直接copy的
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def checkLoginButton(self, event):
        messageBox = QMessageBox()
        messageBox.setIcon(QMessageBox.Information)
        messageBox.setWindowTitle("输入提示")
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        button_inputAgain = messageBox.button(QMessageBox.Yes)
        button_exit = messageBox.button(QMessageBox.No)
        button_inputAgain.setText("重新输入")
        button_exit.setText("退出")

        inputUsername = self.usernameEdit.text().strip()
        inputPassword = self.passwordEdit.text()
        if inputUsername == "":  # 输入的用户名为空或仅有空白符
            messageBox.setText("输入的用户名为空，请重新输入  ")
            messageBox.exec_()
            if messageBox.clickedButton() == button_inputAgain:
                messageBox.close()
            else:  # messageBox.close()
                qApp.exit()
        elif inputPassword == "":
            messageBox.setText("输入的密码为空，请重新输入  ")
            messageBox.exec_()
            if messageBox.clickedButton() == button_inputAgain:
                messageBox.close()
            else:  # messageBox.close()
                qApp.quit()
        elif not usernameExists(inputUsername):  # 输入的用户名不存在
            messageBox.setText("用户名不存在，请重新输入  ")
            messageBox.exec_()
            if messageBox.clickedButton() == button_inputAgain:
                messageBox.close()
            else:  # messageBox.close()
                qApp.exit()
        elif not checkPassword(inputUsername, inputPassword):  # 用户名存在，但密码错误
            messageBox.setText("密码错误，请重新输入  ")
            messageBox.exec_()
            if messageBox.clickedButton() == button_inputAgain:
                messageBox.close()
            else:  # messageBox.close()
                qApp.exit()
        else:  # 用户名存在且密码正确
            qApp.exit()
            loginUser(inputUsername, inputPassword)

    def checkRegisterButton(self, event):
        self.__messageBoxForUsername = QMessageBox()
        self.__messageBoxForUsername.setIcon(QMessageBox.Information)
        self.__messageBoxForUsername.setWindowTitle("输入提示")
        self.__messageBoxForUsername.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.__button_inputAgain = self.__messageBoxForUsername.button(QMessageBox.Yes)
        self.__button_exit = self.__messageBoxForUsername.button(QMessageBox.No)
        self.__button_inputAgain.setText("重新输入")
        self.__button_exit.setText("取消")

        inputNewUsername = self.__inputNewUsername()
        if inputNewUsername is None:
            return
        inputNewPassword = self.__inputNewPassword()
        self.__formerPassword = inputNewPassword
        if inputNewPassword is None:
            return
        inputNewPassword_again = self.__inputNewPassword_again()
        if inputNewPassword_again is None:
            return

        registerUser(inputNewUsername, inputNewPassword)

        messageBox = QMessageBox()
        messageBox.setWindowTitle("提示")
        messageBox.setText("注册成功，点击确认返回登录界面")
        messageBox.setStandardButtons(QMessageBox.Yes)
        button_return = messageBox.button(QMessageBox.Yes)
        button_return.setText("确认")
        messageBox.exec_()
        button_return.clicked.connect(messageBox.close)

    def __inputNewUsername(self):
        inputDialog = QInputDialog()
        inputDialog.setOkButtonText("确认")
        inputDialog.setCancelButtonText("取消")
        inputDialog.setLabelText("请输入新用户名：")
        while inputDialog.exec_():
            __inputNewUsername = inputDialog.textValue().strip()
            if __inputNewUsername == "":  # 输入的用户名为空或仅有空白符
                self.__messageBoxForUsername.setText("输入的用户名为空，请重新输入  ")
                self.__messageBoxForUsername.exec_()
                if self.__messageBoxForUsername.clickedButton() == self.__button_inputAgain:
                    self.__messageBoxForUsername.close()
                else:
                    self.__messageBoxForUsername.close()
                    inputDialog.close()
                    return None
            elif usernameExists(__inputNewUsername):  # 输入的用户名不存在
                self.__messageBoxForUsername.setText("用户名已存在，请重新输入  ")
                self.__messageBoxForUsername.exec_()
                if self.__messageBoxForUsername.clickedButton() == self.__button_inputAgain:
                    self.__messageBoxForUsername.close()
                else:
                    self.__messageBoxForUsername.close()
                    inputDialog.close()
                    return None
            else:
                self.__messageBoxForUsername.close()
                inputDialog.close()
                return __inputNewUsername

    def __inputNewPassword(self):
        inputDialog = QInputDialog()
        inputDialog.setOkButtonText("确认")
        inputDialog.setCancelButtonText("取消")
        inputDialog.setLabelText("请输入密码：")
        while inputDialog.exec_():
            __inputNewPassword = inputDialog.textValue()
            if __inputNewPassword == "":  # 输入的密码为空
                self.__messageBoxForUsername.setText("输入的密码为空，请重新输入  ")
                self.__messageBoxForUsername.exec_()
                if self.__messageBoxForUsername.clickedButton() == self.__button_inputAgain:
                    self.__messageBoxForUsername.close()
                else:
                    self.__messageBoxForUsername.close()
                    inputDialog.close()
                    return None
            else:
                self.__messageBoxForUsername.close()
                inputDialog.close()
                return __inputNewPassword

    def __inputNewPassword_again(self):  # 再输一遍，确认密码
        inputDialog = QInputDialog()
        inputDialog.setOkButtonText("确认")
        inputDialog.setCancelButtonText("取消")
        inputDialog.setLabelText("请再次输入密码：")
        while inputDialog.exec_():
            __inputNewPassword_again = inputDialog.textValue()
            if __inputNewPassword_again == "":  # 输入的密码为空
                self.__messageBoxForUsername.setText("输入的密码为空，请重新输入  ")
                self.__messageBoxForUsername.exec_()
                if self.__messageBoxForUsername.clickedButton() == self.__button_inputAgain:
                    self.__messageBoxForUsername.close()
                else:
                    self.__messageBoxForUsername.close()
                    inputDialog.close()
                    return None
            elif __inputNewPassword_again != self.__formerPassword:
                self.__messageBoxForUsername.setText("输入的密码与前一次不同，请重新输入  ")
                self.__messageBoxForUsername.exec_()
                if self.__messageBoxForUsername.clickedButton() == self.__button_inputAgain:
                    self.__messageBoxForUsername.close()
                else:
                    self.__messageBoxForUsername.close()
                    inputDialog.close()
                    return None
            else:
                self.__messageBoxForUsername.close()
                inputDialog.close()
                return __inputNewPassword_again


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loginWindow = LoginWindow()
    sys.exit(app.exec_())
