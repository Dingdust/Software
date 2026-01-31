import os
import time
import shutil
from typing import Union

import qfluentwidgets as qfw
import qfluentwidgets.multimedia as multimedia
from PyQt6.QtCore import Qt, QRectF, pyqtSignal, QUrl, QSize
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget, QFileDialog, QStackedWidget
from PyQt6.QtGui import QColor, QIcon, QPainter, QPixmap, QDesktopServices, QFont, QDragEnterEvent, QDropEvent, QMouseEvent, QImage


def drawIcon(icon: Union[str, QIcon, qfw.FluentIconBase], painter: QPainter, rect: QRectF, state: QIcon.State = QIcon.State.Off, **attributes) -> None:
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

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._parent = parent
        self.backgroundPixmap = QPixmap(r"./resources/background.png")
        
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
        content: str = "暂不支持本服务！") -> None:
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
        content: str = "暂不支持本服务！") -> None:
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
        content: str = "暂不支持本服务！") -> None:
        qfw.InfoBar.error(
            title=title,
            content=content,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=1000,
            position=qfw.InfoBarPosition.TOP_RIGHT,
            parent=self._parent
        )

    def paintEvent(self, e) -> None:
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
    
    def __init__(self, icon: Union[str, QIcon, qfw.FluentIconBase], title: str, content: str = None, parent=None) -> None:
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

    def paintEvent(self, e) -> None:
        painter = QPainter(self)

        if not self.isEnabled():
            painter.setOpacity(0.36)

        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        drawIcon(self._icon, painter, self.rect())


class EditSettingCard(QFrame):

    clicked = pyqtSignal()

    def __init__(self, icon: Union[str, QIcon, qfw.FluentIconBase], title: str, content: str = None, parent=None, text: str = "AI自动填写") -> None:
        super().__init__(parent=parent)
        self._parent = parent
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

    def paintEvent(self, e) -> None:
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

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self._parent = parent
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

        self.button = qfw.PushButton("AI自动填写", self, qfw.FluentIcon.EDIT)
        self.topLayout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignRight)
        self.topLayout.addSpacing(16)
        self.button.clicked.connect(self.clicked)

    def paintEvent(self, e) -> None:
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

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self._parent = parent
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

        self.button = qfw.PushButton("AI自动填写", self, qfw.FluentIcon.EDIT)
        self.topLayout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignRight)
        self.topLayout.addSpacing(16)
        self.button.clicked.connect(self.clicked)

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        if qfw.isDarkTheme():
            painter.setBrush(QColor(255, 255, 255, 13))
            painter.setPen(QColor(0, 0, 0, 50))
        else:
            painter.setBrush(QColor(255, 255, 255, 170))
            painter.setPen(QColor(0, 0, 0, 19))

        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)


class FileCard(QFrame):
    
    removed = pyqtSignal(str)

    def __init__(self, file_path: str, parent=None) -> None:
        super().__init__(parent)
        self.file_path = file_path
        self._parent = parent
        
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(16, 12, 16, 0)
        self.hBoxLayout.setSpacing(16)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.iconBtn = qfw.TransparentToolButton(qfw.FluentIcon.DOCUMENT, self)
        self.iconBtn.setFixedSize(40, 40)
        self.iconBtn.setIconSize(QSize(24, 24))
        self.iconBtn.setFont(QFont("Segoe UI", 12))
        self.iconBtn.clicked.connect(self.open_file)

        self.infoWidget = QWidget()
        self.infoLayout = QVBoxLayout(self.infoWidget)
        self.infoLayout.setContentsMargins(0, 0, 0, 0)
        self.infoLayout.setSpacing(0)
        
        self.nameLabel = QLabel(os.path.basename(file_path), self)
        self.pathLabel = QLabel(file_path, self)
        self.pathLabel.setStyleSheet("font-size: 12px; color: gray;")

        self.infoLayout.addWidget(self.nameLabel)
        self.infoLayout.addWidget(self.pathLabel)

        self.deleteBtn = qfw.TransparentToolButton(qfw.FluentIcon.CLOSE, self)
        self.deleteBtn.setFixedSize(24, 24)
        self.deleteBtn.setIconSize(QSize(16, 16))
        self.deleteBtn.setFont(QFont("Segoe UI", 12))
        self.deleteBtn.clicked.connect(self.delete_card)

        self.hBoxLayout.addWidget(self.iconBtn)
        self.hBoxLayout.addWidget(self.infoWidget)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.deleteBtn)
        
        self.setFixedHeight(72)
        
    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        if qfw.isDarkTheme():
            painter.setBrush(QColor(255, 255, 255, 13))
            painter.setPen(QColor(0, 0, 0, 50))
        else:
            painter.setBrush(QColor(255, 255, 255, 170))
            painter.setPen(QColor(0, 0, 0, 19))

        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -9), 6, 6)

    def open_file(self) -> None:
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.file_path))

    def delete_card(self) -> None:
        self.removed.emit(self.file_path)
        self.deleteLater()


class FileUploadCard(QFrame):

    def __init__(self, icon: Union[str, QIcon, qfw.FluentIconBase], title: str, content: str = None, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.iconLabel = SettingIconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(content, self)
        
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

        self.fileLayout = QVBoxLayout()
        self.fileLayoutContent = []
        self.fileLayout.setContentsMargins(16, 0, 16, 0)

        self.mainLayout.addLayout(self.fileLayout)

        self.contentLabel.setObjectName('contentLabel')
        qfw.FluentStyleSheet.SETTING_CARD.apply(self)

        self.button = qfw.PushButton("上传PDF文档", self, qfw.FluentIcon.ADD_TO)
        self.topLayout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignRight)
        self.topLayout.addSpacing(16)
        self.button.clicked.connect(self.upload_file)

    def paintEvent(self, e) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        if qfw.isDarkTheme():
            painter.setBrush(QColor(255, 255, 255, 13))
            painter.setPen(QColor(0, 0, 0, 50))
        else:
            painter.setBrush(QColor(255, 255, 255, 170))
            painter.setPen(QColor(0, 0, 0, 19))

        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 6, 6)

    def upload_file(self) -> None:
        fname, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "PDF Files (*.pdf)")
        if fname:
            if fname in self.fileLayoutContent:
                return
            
            self.fileLayoutContent.append(fname)
            card = FileCard(fname, self)
            card.removed.connect(self.remove_file)
            self.fileLayout.addWidget(card)

    def remove_file(self, file_path: str) -> None:
        if file_path in self.fileLayoutContent:
            self.fileLayoutContent.remove(file_path)


class FileUploadArea(QFrame):

    fileMoved = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: transparent;")
        self.setFixedHeight(64)
        
        self.vBoxLayout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap(r"./resources/copyright.png"))
        self.label.setScaledContents(True)
        self.vBoxLayout.addWidget(self.label)
        
        self.treeWidget = None
        self.rootPath = None
        self.enabled = False

    def setContext(self, treeWidget: qfw.TreeWidget, rootPath: str) -> None:
        self.treeWidget = treeWidget
        self.rootPath = rootPath
        self.enabled = True

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if self.enabled and event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        if not self.enabled or not self.rootPath:
            return

        targetPath = self._getCurrentTargetDir()
        
        files_moved = False
        for url in event.mimeData().urls():
            srcPath = url.toLocalFile()
            if os.path.exists(srcPath):
                dstPath = os.path.join(targetPath, os.path.basename(srcPath))
                if srcPath != dstPath:
                    shutil.copy(srcPath, dstPath)
                    files_moved = True
        
        if files_moved:
            self.fileMoved.emit()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if not self.enabled or not self.rootPath:
            return
            
        filePath, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if filePath:
            targetPath = self._getCurrentTargetDir()
            dstPath = os.path.join(targetPath, os.path.basename(filePath))
            if filePath != dstPath:
                shutil.move(filePath, dstPath)
                self.fileMoved.emit()
        
        super().mousePressEvent(event)

    def _getCurrentTargetDir(self) -> str:
        if not self.treeWidget:
            return self.rootPath
            
        item = self.treeWidget.currentItem()
        if item:
            path = item.data(0, Qt.ItemDataRole.UserRole)
            if os.path.isdir(path):
                return path
            else:
                return os.path.dirname(path)
        return self.rootPath


class ClickableWidget(QWidget):

    doubleClicked = pyqtSignal()

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
        super().mouseDoubleClickEvent(event)


class FileDetailStackWidget(QStackedWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setObjectName("fileDetailStackWidget")
        self.setStyleSheet("background-color: transparent;")

        self.textContainer = qfw.TextEdit(self)
        self.textContainer.setReadOnly(True)

        self.imageContainer = ClickableWidget(self)
        self.imageLayout = QVBoxLayout(self.imageContainer)
        self.imageLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageWrapper = qfw.ImageLabel(self.imageContainer)
        self.imageLayout.addWidget(self.imageWrapper)

        self.audioContainer = ClickableWidget(self)
        self.audioLayout = QVBoxLayout(self.audioContainer)
        self.audioLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.audioWrapper = multimedia.StandardMediaPlayBar(self.audioContainer)
        self.audioWrapper.volumeButton.setFont(QFont("Segoe UI", 12))
        self.audioWrapper.skipBackButton.setFont(QFont("Segoe UI", 12))
        self.audioWrapper.playButton.setFont(QFont("Segoe UI", 12))
        self.audioWrapper.skipForwardButton.setFont(QFont("Segoe UI", 12))
        self.mediaPlayer = multimedia.MediaPlayer(self)
        self.audioWrapper.setMediaPlayer(self.mediaPlayer)
        self.audioLayout.addWidget(self.audioWrapper)

        self.videoContainer = multimedia.VideoWidget(self)
        self.videoContainer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.addWidget(self.textContainer)
        self.addWidget(self.imageContainer)
        self.addWidget(self.audioContainer)
        self.addWidget(self.videoContainer)

    def updateFile(self, path: str) -> None:
        self.mediaPlayer.stop()
        self.videoContainer.pause()

        if not os.path.exists(path):
            self.textContainer.setText("File not found.")
            self.setCurrentIndex(0)
        elif os.path.isdir(path):
            self.showDefaultInfo(path)
        else:
            ext = os.path.splitext(path)[1].lower()
            source = QUrl.fromLocalFile(path)
            if ext in ['.txt', '.py', '.json', '.md', '.js', '.html', '.css', '.sh', '.bat']:
                try:
                    with open(path, encoding="utf-8") as file:
                        content = file.read()
                    self.textContainer.setText(content)
                    self.setCurrentIndex(0)
                except Exception:
                    self.showDefaultInfo(path)
            elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.ico', '.svg']:
                image = QImage(path)
                if image.width() > image.height():
                    image = image.scaledToWidth(512) if image.width() > 512 else image
                else:
                    image = image.scaledToHeight(512) if image.height() > 512 else image
                self.imageWrapper.setImage(image)
                self.imageContainer.doubleClicked.connect(lambda: QDesktopServices.openUrl(source))
                self.setCurrentIndex(1)
            elif ext in ['.mp3', '.wav', '.flac', '.m4a']:
                self.mediaPlayer.setSource(source)
                self.audioContainer.doubleClicked.connect(lambda: QDesktopServices.openUrl(source))
                self.setCurrentIndex(2)
            elif ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv']:
                self.videoContainer.setVideo(source)
                self.setCurrentIndex(3)
                self.videoContainer.play()
            else:
                self.showDefaultInfo(path)

    def showDefaultInfo(self, path: str) -> None:
        try:
            size = os.path.getsize(path)
            ctime = os.path.getctime(path)
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ctime))
            info = f"Path: {path}\nSize: {size} bytes\nCreated: {time_str}"
        except Exception:
            info = f"Path: {path}"

        self.textContainer.setText(info)
        self.setCurrentIndex(0)