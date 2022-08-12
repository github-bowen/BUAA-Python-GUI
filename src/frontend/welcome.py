import os.path
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie, QPalette
from PyQt5.QtWidgets import qApp, QLabel, QApplication, QWidget, QSizePolicy


class Welcome(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowStaysOnTopHint)  # 置顶
        self.setWindowFlags(Qt.FramelessWindowHint)  # 不显示标题栏啥的

        # 加载gif, 调整大小
        self.welcomeLabel = QLabel(self)
        self.welcomeLabel.setBackgroundRole(QPalette.Base)
        self.welcomeLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.welcomeLabel.setScaledContents(True)  # QMovie适应QLabel大小

        self.welcomeMovie = QMovie("../img/welcome.gif")
        self.welcomeLabel.setMovie(self.welcomeMovie)
        self.welcomeLabel.resize(750, 550)
        # self.welcomeLabel.adjustSize()
        self.welcomeMovie.start()

        # 定时关闭
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.closeAll)  # 计时结束调用operate()方法
        self.timer.start(3000)  # 设置计时间隔并启动 3s后关闭窗口

        self.show()

    def closeAll(self):
        self.close()
        qApp.exit()


if __name__ == '__main__':
    show_welcome = True  # 默认展示欢迎gif
    if not os.path.exists(".welcome.log"):
        with open(".welcome.log", "w") as f:
            print(True, file=f)  # 默认要显示欢迎gif
    else:
        with open(".welcome.log", "r") as f:
            show_welcome = eval(f.read().strip())

    if show_welcome:
        app = QApplication(sys.argv)
        welcome = Welcome()
        app.exec_()
        app.closeAllWindows()

    os.system("python ./login.py")
