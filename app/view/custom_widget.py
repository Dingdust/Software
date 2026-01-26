from typing import Union

import qfluentwidgets as qfw
from PyQt6.QtCore import Qt, QRectF, pyqtSignal
from PyQt6.QtGui import QColor, QIcon, QPainter
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget


def drawIcon(icon, painter, rect, state=QIcon.State.Off, **attributes):
    if isinstance(icon, qfw.FluentIconBase):
        icon.render(painter, rect, **attributes)
    elif isinstance(icon, qfw.Icon):
        icon.fluentIcon.render(painter, rect, **attributes)
    else:
        icon = QIcon(icon)
        icon.paint(painter, QRectF(rect).toRect(), Qt.AlignmentFlag.AlignCenter, state=state)


class SettingIconWidget(qfw.IconWidget):

    def paintEvent(self, e):
        painter = QPainter(self)

        if not self.isEnabled():
            painter.setOpacity(0.36)

        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        drawIcon(self._icon, painter, self.rect())


class EditSettingCard(QFrame):

    clicked = pyqtSignal()

    def __init__(self, icon: Union[str, QIcon, qfw.FluentIconBase], title: str, content=None, parent=None, text: str = "AI自动填写"):
        super().__init__(parent=parent)
        self.iconLabel = SettingIconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(content or '', self)
        
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        
        self.topWidget = QWidget()
        self.topWidget.setFixedHeight(70)
        self.topLayout = QHBoxLayout(self.topWidget)
        
        self.vBoxLayout = QVBoxLayout()

        if not content:
            self.contentLabel.hide()

        self.iconLabel.setFixedSize(16, 16)

        self.topLayout.setSpacing(0)
        self.topLayout.setContentsMargins(16, 0, 0, 0)
        self.topLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.topLayout.addWidget(self.iconLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.topLayout.addSpacing(16)

        self.topLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignLeft)

        self.topLayout.addSpacing(16)
        self.topLayout.addStretch(1)
        
        self.mainLayout.addWidget(self.topWidget)
        
        self.plainTextEdit = qfw.PlainTextEdit(self)
        self.plainTextEdit.setFixedHeight(100)
        
        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setContentsMargins(16, 0, 16, 16)
        self.bottomLayout.addWidget(self.plainTextEdit)
        self.mainLayout.addLayout(self.bottomLayout)

        self.contentLabel.setObjectName('contentLabel')
        self.setFixedHeight(186 if content else 166)
        qfw.FluentStyleSheet.SETTING_CARD.apply(self)

        self.button = qfw.PushButton(text, self, qfw.FluentIcon.EDIT)
        self.topLayout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignRight)
        self.topLayout.addSpacing(16)
        self.button.clicked.connect(self.clicked)

    def setTitle(self, title: str):
        self.titleLabel.setText(title)

    def setContent(self, content: str):
        self.contentLabel.setText(content)
        self.contentLabel.setVisible(bool(content))

    def setIconSize(self, width: int, height: int):
        self.iconLabel.setFixedSize(width, height)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        if qfw.isDarkTheme():
            painter.setBrush(QColor(255, 255, 255, 13))
            painter.setPen(QColor(0, 0, 0, 50))
        else:
            painter.setBrush(QColor(255, 255, 255, 170))
            painter.setPen(QColor(0, 0, 0, 19))

        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)


class DevLanguageCard(QFrame):

    clicked = pyqtSignal()

    def __init__(self, parent=None, text: str = "AI自动填写"):
        super().__init__(parent=parent)
        self.iconLabel = SettingIconWidget(qfw.FluentIcon.LANGUAGE, self)
        self.titleLabel = QLabel("编程语言", self)
        self.contentLabel = QLabel("若有需要，请输入其他编程语言...（120字）", self)
        
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        
        self.topWidget = QWidget()
        self.topWidget.setFixedHeight(70)
        self.topLayout = QHBoxLayout(self.topWidget)
        
        self.vBoxLayout = QVBoxLayout()

        self.iconLabel.setFixedSize(16, 16)

        self.topLayout.setSpacing(0)
        self.topLayout.setContentsMargins(16, 0, 0, 0)
        self.topLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.topLayout.addWidget(self.iconLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.topLayout.addSpacing(16)

        self.topLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignLeft)

        self.topLayout.addSpacing(16)
        self.topLayout.addStretch(1)
        
        self.mainLayout.addWidget(self.topWidget)

        self.tags = ["Assembly language", "C", "C#"]
        self.tagLayout = qfw.FlowLayout()
        self.tagLayout.setContentsMargins(16, 0, 16, 0)
        for tag in self.tags:
            self.tagLayout.addWidget(qfw.ToggleButton(tag))

        self.mainLayout.addLayout(self.tagLayout)
        
        self.plainTextEdit = qfw.PlainTextEdit(self)
        self.plainTextEdit.setFixedHeight(100)
        
        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setContentsMargins(16, 0, 16, 16)
        self.bottomLayout.addWidget(self.plainTextEdit)
        self.mainLayout.addSpacing(16)
        self.mainLayout.addLayout(self.bottomLayout)

        self.contentLabel.setObjectName('contentLabel')
        qfw.FluentStyleSheet.SETTING_CARD.apply(self)

        self.button = qfw.PushButton(text, self, qfw.FluentIcon.EDIT)
        self.topLayout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignRight)
        self.topLayout.addSpacing(16)
        self.button.clicked.connect(self.clicked)

    def setTitle(self, title: str):
        self.titleLabel.setText(title)

    def setContent(self, content: str):
        self.contentLabel.setText(content)
        self.contentLabel.setVisible(bool(content))

    def setIconSize(self, width: int, height: int):
        self.iconLabel.setFixedSize(width, height)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        if qfw.isDarkTheme():
            painter.setBrush(QColor(255, 255, 255, 13))
            painter.setPen(QColor(0, 0, 0, 50))
        else:
            painter.setBrush(QColor(255, 255, 255, 170))
            painter.setPen(QColor(0, 0, 0, 19))

        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)
