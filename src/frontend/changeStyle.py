from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QStyleFactory


def run(widget: QWidget, who: str, width: int, height: int):
    """
    who = "login": 登录页面
    who = "calendar": 日历页面
    """
    QApplication.setStyle(QStyleFactory.keys()[0])  # TODO:这里可以选择0-3三种样式，不知道windows系统上哪个好看
    widget.setWindowOpacity(0.9)  # 透明度
    # widget.setWindowFlags(Qt.WindowContextHelpButtonHint)

    palette = QPalette()
    if who == "login":  # 设置登录页面背景
        palette.setBrush(QPalette.Background, QBrush(QPixmap("../img/登录背景.jpg")))
    else:  # 设置日历页面背景
        # palette.setBrush(QPalette.Background, QBrush(QPixmap("../img/日历背景.webp")))
        pass  # TODO:日历界面好像不好放背景图，感觉放上去大部分都被挡住了，不好看
    widget.setPalette(palette)
