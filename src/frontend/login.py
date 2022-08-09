import re
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import qApp, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QApplication, QDesktopWidget, \
    QWidget, QMessageBox, QInputDialog, QCheckBox

from src.backend.method import *


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 是否登录成功
        self.loginSuccess = False

        # 是否记住密码的勾选框
        self.rememberPasswordBox = QCheckBox("记住密码")
        self.rememberPasswordBox.toggle()

        # 用户名密码
        self.username = None
        self.password = None

        # 创建标题文字
        self.title = QLabel('欢迎使用任务调度-管理系统！')
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setFamily("KaiTi")
        self.title.setFont(font)

        # 创建标签、文本框、按钮
        self.usernameLabel = QLabel('用户名：')
        self.passwordLabel = QLabel('密码：')

        self.usernameEdit = QLineEdit()
        self.usernameEdit.setPlaceholderText("用户名两侧的空格会自动忽略")
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setPlaceholderText("密码6-15位，只能有数字和字母，两侧空格会自动忽略")
        self.passwordEdit.setEchoMode(QLineEdit.Password)  # 设置密码输入框，不显示输入字符，显示圆点

        self.loginButton = QPushButton('登录')
        self.registerButton = QPushButton('注册')

        # 以__开头的变量或函数为个人内部或临时的变量或函数，不用在意！！！
        self.__messageBoxForUsername = None
        self.__button_inputAgain = None
        self.__button_exit = None
        self.__formerPassword = None

        self.checkIfRememberPassword()
        self.initUI()

    def checkIfRememberPassword(self):
        # 检查 上次登录的时候是否勾选了记住密码
        self.usernameEdit.setText(formerUsername)
        if rememberPasswordBefore:
            self.passwordEdit.setText(formerPassword)

    def changeRememberBox(self, state):
        global rememberPasswordNow
        if state == Qt.Checked:
            rememberPasswordNow = True
        else:
            rememberPasswordNow = False

    def initUI(self):
        # 布局用户名和密码的label和输入框
        grid = QGridLayout()
        grid.setSpacing(5)
        grid.addWidget(self.title, 0, 2, 4, 2)
        grid.addWidget(self.usernameLabel, 4, 0)
        grid.addWidget(self.usernameEdit, 4, 1, 1, 3)
        grid.addWidget(self.passwordLabel, 5, 0)
        grid.addWidget(self.passwordEdit, 5, 1, 1, 3)
        grid.addWidget(self.rememberPasswordBox, 6, 2)

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
        # 设置"记住密码"勾选后的事件
        self.rememberPasswordBox.stateChanged.connect(self.changeRememberBox)

        # 布局整个窗口
        grid.addLayout(vBox, 8, 3)
        self.setLayout(grid)
        self.resize(450, 200)
        self.center()
        self.setWindowTitle("任务调度器-登录")
        self.show()

    def center(self):  # 让当前窗口居中，该部分直接copy的
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @staticmethod
    def __allAlphaOrDigit(s: str):
        pattern = re.compile(r"^[a-zA-Z\d]+$")
        if pattern.match(s):
            return True
        return False

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
        inputPassword = self.passwordEdit.text().strip()
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
            self.loginSuccess = True
            self.username = inputUsername
            self.password = inputPassword

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
        inputDialog.setInputMode(QInputDialog.TextInput)
        inputDialog.setOkButtonText("确认")
        inputDialog.setCancelButtonText("取消")
        inputDialog.setLabelText("请输入新用户名：")
        lineEdit = inputDialog.findChild(QLineEdit)
        lineEdit.setPlaceholderText("用户名两侧的空格会自动忽略")
        inputDialog.resize(360, 200)

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
        inputDialog.setInputMode(QInputDialog.TextInput)
        inputDialog.setOkButtonText("确认")
        inputDialog.setCancelButtonText("取消")
        inputDialog.setLabelText("请输入密码：")
        lineEdit = inputDialog.findChild(QLineEdit)
        lineEdit.setEchoMode(QLineEdit.Password)
        lineEdit.setPlaceholderText("密码6-15位，只能有数字和字母，两侧空格会自动忽略")
        inputDialog.resize(360, 200)

        while inputDialog.exec_():
            __inputNewPassword = inputDialog.textValue().strip()
            if __inputNewPassword == "":  # 输入的密码为空
                self.__messageBoxForUsername.setText("输入的密码为空，请重新输入  ")
                self.__messageBoxForUsername.exec_()
                if self.__messageBoxForUsername.clickedButton() == self.__button_inputAgain:
                    self.__messageBoxForUsername.close()
                else:
                    self.__messageBoxForUsername.close()
                    inputDialog.close()
                    return None
            elif not LoginWindow.__allAlphaOrDigit(__inputNewPassword):
                self.__messageBoxForUsername.setText("输入的密码包含字母数字以外的字符，请重新输入  ")
                self.__messageBoxForUsername.exec_()
                if self.__messageBoxForUsername.clickedButton() == self.__button_inputAgain:
                    self.__messageBoxForUsername.close()
                else:
                    qApp.quit()
            elif not 6 <= len(__inputNewPassword) <= 15:
                self.__messageBoxForUsername.setText("输入的密码长度不在6～15之间，请重新输入  ")
                self.__messageBoxForUsername.exec_()
                if self.__messageBoxForUsername.clickedButton() == self.__button_inputAgain:
                    self.__messageBoxForUsername.close()
                else:
                    qApp.quit()
            else:
                self.__messageBoxForUsername.close()
                inputDialog.close()
                return __inputNewPassword

    def __inputNewPassword_again(self):  # 再输一遍，确认密码
        inputDialog = QInputDialog()
        inputDialog.setInputMode(QInputDialog.TextInput)
        inputDialog.setOkButtonText("确认")
        inputDialog.setCancelButtonText("取消")
        inputDialog.setLabelText("请再次输入密码：")
        lineEdit = inputDialog.findChild(QLineEdit)
        lineEdit.setEchoMode(QLineEdit.Password)
        lineEdit.setPlaceholderText("请输入与上一次相同的密码")
        inputDialog.resize(360, 200)
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
    rememberPasswordBefore = False
    # 判断是否勾选了"记住密码"，若是，则需要在文件".login.log"中记录
    if not os.path.exists(".login.log"):
        with open(".login.log", "w") as f:
            print(False, file=f)  # 默认不记住密码
            print("", file=f)  # 前一次选择自动登录的用户名为None
            print("", file=f)  # 前一次选择自动登录的密码为None
        formerUsername, formerPassword = "", ""
    else:
        with open(".login.log", "r") as f:
            rememberPasswordBefore, formerUsername, formerPassword = f.readlines()
            rememberPasswordBefore = eval(rememberPasswordBefore)
    rememberPasswordNow = True
    formerUsername, formerPassword = formerUsername.strip(), formerPassword.strip()

    app = QApplication(sys.argv)
    loginWindow = LoginWindow()
    app.exec_()
    app.closeAllWindows()

    if loginWindow.loginSuccess:  # 程序结束是否是因为登录成功而结束
        # 临时存储用户名和密码，供calendar.py使用
        with open(".name_password.tmp", "w") as f:
            print(loginWindow.username, file=f)
            print(loginWindow.password, file=f)

        # 判断是否勾选了"记住密码"，若是，则需要在文件".login.log"中记录
        if rememberPasswordNow:  # 勾选了，记录用户名和密码
            with open(".login.log", "w") as f:
                print(True, file=f)
                print(loginWindow.username, file=f)
                print(loginWindow.password, file=f)
        else:  # 没勾选，只记录用户名！！！
            with open(".login.log", "w") as f:
                print(False, file=f)
                print(loginWindow.username, file=f)
                print("", file=f)

        os.system("python ./calendarFront.py")
    else:
        exit(0)
