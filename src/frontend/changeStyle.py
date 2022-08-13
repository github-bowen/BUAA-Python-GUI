from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QStyleFactory, QLabel, QSizePolicy


def run(widget: QWidget, who: str, width: int, height: int):
    """
    who = "login": 登录页面
    who = "calendar": 日历页面
    """
    backGroundLabel = QLabel(widget)
    backGroundLabel.setBackgroundRole(QPalette.Base)
    backGroundLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
    backGroundLabel.setScaledContents(True)  # QMovie适应QLabel大小

    QApplication.setStyle(QStyleFactory.keys()[0])  # TODO:这里可以选择0-3三种样式，不知道windows系统上哪个好看
    widget.setWindowOpacity(1)  # 透明度
    # widget.setWindowFlags(Qt.WindowContextHelpButtonHint)

    if who == "login":  # 设置登录页面背景
        backGroundLabel.setPixmap(QPixmap("../img/loginBG.png"))
        backGroundLabel.resize(width, height)
    else:  # 设置日历页面背景
        # backGroundLabel.setPixmap(QPixmap("../img/日历背景.webp"))
        pass  # TODO:日历界面好像不好放背景图，感觉放上去大部分都被挡住了，不好看
