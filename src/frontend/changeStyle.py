from PyQt5.QtGui import QPalette, QPixmap
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

    # 感觉2比较好看
    QApplication.setStyle(QStyleFactory.keys()[2])  # TODO:这里可以选择0-3三种样式，不知道windows系统上哪个好看
    # widget.setWindowOpacity(0.5)  # 透明度
    # widget.setWindowFlags(Qt.WindowContextHelpButtonHint)

    if who == "login":  # 设置登录页面背景
        backGroundLabel.setPixmap(QPixmap("../img/loginBG.png"))
        backGroundLabel.resize(width, height)
    elif who == 'calendar':  # 设置日历页面背景
        backGroundLabel.setStyleSheet('''QWidget{background-color:#FFFFFF;}''')
        # backGroundLabel.setPixmap(QPixmap("../img/p3.jpg"))
        backGroundLabel.resize(width, height)
        # backGroundLabel.setWindowOpacity(1)
        pass  # TODO:日历界面好像不好放背景图，感觉放上去大部分都被挡住了，不好看
    '''
        elif who == 'dispatch':
        print('can in run')
        backGroundLabel.setPixmap(QPixmap("../img/loginBG.png"))
        backGroundLabel.resize(width, height)
    '''
