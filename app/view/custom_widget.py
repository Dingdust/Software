from typing import Union

import qfluentwidgets as qfw
from PyQt6.QtCore import Qt, QRectF, pyqtSignal
from PyQt6.QtGui import QColor, QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget


def drawIcon(icon, painter, rect, state=QIcon.State.Off, **attributes):
    if isinstance(icon, qfw.FluentIconBase):
        icon.render(painter, rect, **attributes)
    elif isinstance(icon, qfw.Icon):
        icon.fluentIcon.render(painter, rect, **attributes)
    else:
        icon = QIcon(icon)
        icon.paint(painter, QRectF(rect).toRect(), Qt.AlignmentFlag.AlignCenter, state=state)


class BaseSubPage(QWidget):
    
    nextSignal = pyqtSignal()
    prevSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.backgroundPixmap = QPixmap("./resources/background.png")
        
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(20)

        self.scrollArea = qfw.SingleDirectionScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setStyleSheet("background-color: transparent; border: none;")
        
        self.scrollWidget = QWidget()
        self.scrollWidget.setStyleSheet("background-color: transparent;")
        
        self.contentLayout = QVBoxLayout(self.scrollWidget)
        self.contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scrollArea.setWidget(self.scrollWidget)
        
        self.vBoxLayout.addWidget(self.scrollArea)

        self.buttonLayout = QHBoxLayout()
        self.prevBtn = qfw.PushButton("上一步", self)
        self.prevBtn.setFixedWidth(120)
        self.nextBtn = qfw.PrimaryPushButton("下一步", self)
        self.nextBtn.setFixedWidth(120)
        
        self.prevBtn.clicked.connect(self.prevSignal)
        self.nextBtn.clicked.connect(self.nextSignal)
        
        self.buttonLayout.addWidget(self.prevBtn)
        self.buttonLayout.addSpacing(20)
        self.buttonLayout.addWidget(self.nextBtn)
        self.buttonLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.vBoxLayout.addLayout(self.buttonLayout)

    def show_info(
        self, 
        title: str = "提示",
        content: str = "暂不支持本服务！"):
        qfw.InfoBar.info(
            title=title,
            content=content,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=1000,
            position=qfw.InfoBarPosition.TOP_RIGHT,
            parent=self._parent
        )

    def show_warning(
        self, 
        title: str = "提示",
        content: str = "暂不支持本服务！"):
        qfw.InfoBar.warning(
            title=title,
            content=content,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=1000,
            position=qfw.InfoBarPosition.TOP_RIGHT,
            parent=self._parent
        )

    def show_error(
        self, 
        title: str = "提示",
        content: str = "暂不支持本服务！"):
        qfw.InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=1000,
            position=qfw.InfoBarPosition.TOP_RIGHT,
            parent=self._parent
        )

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setOpacity(0.08)
        
        pixmap = self.backgroundPixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        x = int((self.width() - pixmap.width()) / 2)
        y = int((self.height() - pixmap.height()) / 2)
        painter.drawPixmap(x, y, pixmap)


class IdentityCard(qfw.ElevatedCardWidget):
    
    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.setClickEnabled(True)
        self.setFixedSize(320, 240)
        
        self.vLayout = QVBoxLayout(self)
        self.vLayout.setSpacing(20)
        self.vLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.iconWidget = qfw.IconWidget(icon, self)
        self.iconWidget.setFixedSize(64, 64)
        
        self.titleLabel = qfw.SubtitleLabel(title, self)
        self.contentLabel = qfw.BodyLabel(content, self)
        self.contentLabel.setTextColor(Qt.GlobalColor.gray, Qt.GlobalColor.gray)

        self.vLayout.addWidget(self.iconWidget, 0, Qt.AlignmentFlag.AlignCenter)
        self.vLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignCenter)
        self.vLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignCenter)


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

        self.tags = ["Assembly language", "C", "C#", "C++", "Delphi/Object Pascal", "Go", "HTML",
                     "Java", "JavaScript", "MATLAB", "Objective-C", "PHP", "PL/SQL", "Perl",
                     "Python", "R", "Ruby", "SQL", "Swift", "Visual Basic", "Visual Basic .Net"] 
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


class FeaturesCard(QFrame):

    clicked = pyqtSignal()

    def __init__(self, parent=None, text: str = "AI自动填写"):
        super().__init__(parent=parent)
        self.iconLabel = SettingIconWidget(qfw.FluentIcon.LEAF, self)
        self.titleLabel = QLabel("软件的技术特点", self)
        self.contentLabel = QLabel("请输入...（100字）", self)
        
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

        self.tags = ["APP", "游戏软件", "教育软件", "金融软件", "医疗软件", "地理信息软件", "云计算软件", "信息安全软件",
                     "大数据软件", "人工智能软件", "VR软件", "5G软件", "小程序", "物联网软件", "智慧城市软件"] 
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


class CodeIdentityCard(qfw.ExpandGroupSettingCard):

    def __init__(self, parent=None):
        super().__init__(qfw.FluentIcon.COMMAND_PROMPT, "程序鉴别材料", "请上传pdf格式。", parent)
