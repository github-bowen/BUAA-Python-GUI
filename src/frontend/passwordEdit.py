from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon, QCursor, QFocusEvent, QPixmap
from PyQt5.QtWidgets import QLineEdit, QAction, QToolButton


class PasswordEdit(QLineEdit):
    def __init__(self, text):
        super().__init__()
        self.setEchoMode(QLineEdit.Password)  # 设置密码输入框，不显示输入字符，显示圆点
        self.setPlaceholderText(text)
        self.setClearButtonEnabled(True)
        self.eyeOn, self.eyeOff = QIcon(), QIcon()
        # self.eyeOn.addPixmap(QPixmap(":/eyeOn"))  # todo: 这个眼睛图标怪怪的
        # self.eyeOff.addPixmap(QPixmap(":/eyeOff"))
        self.eyeOn.addPixmap(QPixmap("../Icon/eyeOn.png"))
        self.eyeOff.addPixmap(QPixmap("../Icon/eyeOff.png"))
        action = QAction(self.eyeOn, "显示密码", self)
        self.addAction(action, QLineEdit.TrailingPosition)
        self.showPasswordButton = QToolButton(action.associatedWidgets()[-1])
        # print(action.associatedWidgets())
        # self.showPasswordButton.setIcon()
        self.showPasswordButton.hide()
        self.showPasswordButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.showPasswordButton.pressed.connect(self.onPressed)
        self.showPasswordButton.released.connect(self.onReleased)

    def onPressed(self):
        button = QToolButton(self.sender())
        button.setIcon(self.eyeOn)
        self.setEchoMode(QLineEdit.Normal)

    def onReleased(self):
        button = QToolButton(self.sender())
        button.setIcon(self.eyeOff)
        self.setEchoMode(QLineEdit.Password)

    def enterEvent(self, a0: QEvent) -> None:  # 重载方法
        self.showPasswordButton.show()
        super(PasswordEdit, self).enterEvent(a0)

    def leaveEvent(self, a0: QEvent) -> None:  # 重载方法
        self.showPasswordButton.hide()
        super(PasswordEdit, self).leaveEvent(a0)

    def focusInEvent(self, a0: QFocusEvent) -> None:  # 重载方法
        self.showPasswordButton.show()
        super(PasswordEdit, self).focusInEvent(a0)

    def focusOutEvent(self, a0: QFocusEvent) -> None:  # 重载方法
        self.showPasswordButton.hide()
        super(PasswordEdit, self).focusOutEvent(a0)

