import re
import sys

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import qApp, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QHBoxLayout, QApplication, QDesktopWidget, \
    QWidget, QMessageBox, QInputDialog, QCheckBox, QFrame, QSplitter, QSizePolicy

from src.backend.method import *
from passwordEdit import PasswordEdit
import changeStyle


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.width, self.height = 800, 450
        changeStyle.run(self, "login", self.width, self.height)

        # 是否登录成功
        self.loginSuccess = False

        self.fontSize = 12
        # 是否记住密码的勾选框
        self.rememberPasswordBox = QCheckBox("记住密码")
        font = QFont()
        font.setPointSize(self.fontSize)
        self.rememberPasswordBox.setFont(font)
        if rememberPasswordBefore:
            self.rememberPasswordBox.toggle()

        # 是否显示登录动画
        self.displayGifBox = QCheckBox("显示欢迎动画")
        font = QFont()
        font.setPointSize(self.fontSize)
        self.displayGifBox.setFont(font)
        if displayGif:
            self.displayGifBox.toggle()

        # 用户名密码
        self.username = None
        self.password = None

        # 创建标题文字
        """
        self.title = QLabel('欢迎使用任务调度-管理系统！')
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        # font.setFamily("KaiTi")
        self.title.setFont(font)
        """

        # 创建标签、文本框、按钮
        self.usernameIcon=QLabel()
        # todo:加了个图标 看在你们电脑上效果咋样
        self.usernameIcon.setPixmap(QPixmap("../Icon/用户.svg").scaled(40,40))
        self.usernameLabel = QLabel('用户名:')
        font = QFont()
        font.setPointSize(self.fontSize)
        self.usernameLabel.setFont(font)
        self.passwordIcon = QLabel()
        self.passwordIcon.setPixmap(QPixmap("../Icon/密码.svg").scaled(40,40))
        self.passwordLabel = QLabel('密码:')
        font = QFont()
        font.setPointSize(self.fontSize)
        self.passwordLabel.setFont(font)

        self.usernameEdit = QLineEdit()
        lineEditWidth = self.usernameEdit.width()
        self.usernameEdit.setFixedWidth(int(lineEditWidth / 2.6))
        font = QFont()
        font.setPointSize(self.fontSize)
        self.usernameEdit.setFont(font)
        self.usernameEdit.setClearButtonEnabled(True)
        self.usernameEdit.setPlaceholderText("用户名两侧的空格会自动忽略")

        self.passwordEdit = PasswordEdit("密码6-15位，只能有数字和字母，忽略两侧空格")
        self.passwordEdit.setFixedWidth(int(lineEditWidth / 2.6))
        font = QFont()
        font.setPointSize(self.fontSize)
        self.passwordEdit.setFont(font)

        self.loginButton = QPushButton('登录')
        self.loginButton.setFixedSize(100, 50)
        font = QFont()
        font.setPointSize(self.fontSize)
        self.loginButton.setFont(font)
        self.registerButton = QPushButton('注册')
        self.registerButton.setFixedSize(100, 50)
        font = QFont()
        font.setPointSize(self.fontSize)
        self.registerButton.setFont(font)

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

    def changeDisplayGifBox(self, state):
        global displayGif
        if state == Qt.Checked:
            displayGif = True
        else:
            displayGif = False

    def initUI(self):
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

        hBox = QHBoxLayout(self)

        left = QFrame(self)
        left.setFrameShape(QFrame.StyledPanel)
        left.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        right = QFrame(self)
        right.setFrameShape(QFrame.StyledPanel)
        right.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        farRight = QFrame(self)  # 最右边的分割，防止输入框超出白色格子
        farRight.setFrameShape(QFrame.StyledPanel)

        splitter = QSplitter(Qt.Horizontal)
        # splitter.show()
        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.addWidget(farRight)
        splitter.setSizes((300, 200, 40))
        # splitter.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed) #TODO：看看怎么不让拉伸

        hBox.addWidget(splitter)
        self.setLayout(hBox)

        # 布局用户名和密码的label和输入框
        grid = QGridLayout()
        grid.setSpacing(10)
        grid.setVerticalSpacing(10)

        topEmpty = QLineEdit()
        topEmpty.setFixedWidth(0)
        # topEmptyLabel.setFixedHeight(100)
        grid.addWidget(topEmpty, 0, 0)
        #grid.addWidget(self.usernameIcon, 1, 0)
        grid.addWidget(self.usernameLabel, 1, 0)
        grid.addWidget(self.usernameEdit, 1, 1, 1, 3)
        #grid.addWidget(self.passwordIcon, 2, 0)
        grid.addWidget(self.passwordLabel, 2, 0)
        grid.addWidget(self.passwordEdit, 2, 1, 1, 3)
        grid.addWidget(self.rememberPasswordBox, 3, 0)
        grid.addWidget(self.displayGifBox, 3, 1)
        grid.addWidget(self.loginButton, 4, 1)
        grid.addWidget(self.registerButton, 4, 2)

        """
        # 布局登录和注册按钮
        hBox = QHBoxLayout()
        hBox.addStretch(1)
        hBox.addWidget(self.loginButton)
        hBox.addWidget(self.registerButton)

        vBox = QVBoxLayout()
        vBox.addStretch(1)
        vBox.addLayout(hBox)

        # 布局整个窗口
        grid.addLayout(vBox, 9, 1)
        """
        right.setLayout(grid)

        # 设置事件
        # 设置"登录"Button点击后的事件
        self.loginButton.clicked.connect(self.checkLoginButton)
        # 设置"注册"Button点击后的事件
        self.registerButton.clicked.connect(self.checkRegisterButton)
        # 设置"记住密码"勾选后的事件
        self.rememberPasswordBox.stateChanged.connect(self.changeRememberBox)
        self.displayGifBox.stateChanged.connect(self.changeDisplayGifBox)

        self.resize(self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.center()
        self.setWindowTitle("任务管理器-登录")
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
        lineEdit.setClearButtonEnabled(True)
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
        lineEdit.setPlaceholderText("密码6-15位，只能有数字和字母，两侧空格会自动忽略")
        lineEdit.setClearButtonEnabled(True)
        lineEdit.setEchoMode(QLineEdit.Password)
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
        lineEdit.setPlaceholderText("请输入与上一次相同的密码")
        lineEdit.setClearButtonEnabled(True)
        lineEdit.setEchoMode(QLineEdit.Password)
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

    with open(".welcome.log", "r") as f:
        displayGif = eval(f.read().strip())

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

        # 更改下次打开时是否显示启动动画
        with open(".welcome.log", "w") as f:
            f.write(str(displayGif))

        os.system("python ./calendarFront.py")
    else:
        exit(0)
