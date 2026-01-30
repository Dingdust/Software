import os
import time
import shutil
from typing import Union

import qfluentwidgets as qfw
from PyQt6.QtCore import Qt, QRectF, pyqtSignal, QUrl, QSize
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget, QFileDialog, QStackedWidget
from PyQt6.QtGui import QColor, QIcon, QPainter, QPixmap, QDesktopServices, QFont, QDragEnterEvent, QDropEvent, QMouseEvent


from qfluentwidgets.multimedia import StandardMediaPlayBar, VideoWidget


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


class FileDetailStackWidget(QStackedWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setObjectName("fileDetailStackWidget")
        self.setStyleSheet("background-color: transparent;")

        self.textEdit = qfw.TextEdit(self)
        self.textEdit.setReadOnly(True)

        self.imageContainer = QWidget(self)
        self.imageLayout = QVBoxLayout(self.imageContainer)
        self.imageLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageLabel = qfw.ImageLabel(self)
        self.imageLabel.setBorderRadius(8, 8, 8, 8)
        self.imageLayout.addWidget(self.imageLabel)

        self.audioContainer = QWidget(self)
        self.audioLayout = QVBoxLayout(self.audioContainer)
        self.audioLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.videoWidget = VideoWidget(self)
        self.mediaPlayer = self.videoWidget.player

        self.mediaPlayBar = StandardMediaPlayBar(self)
        self.audioLayout.addWidget(self.mediaPlayBar)
        self.mediaPlayBar.setFixedWidth(600)

        self.mediaPlayBar.playButton.clicked.connect(self.toggleAudioPlayState)
        self.mediaPlayBar.progressSlider.valueChanged.connect(self.onSliderValueChanged)
        self.mediaPlayer.positionChanged.connect(self.onAudioPositionChanged)
        self.mediaPlayer.durationChanged.connect(self.onAudioDurationChanged)
        self.mediaPlayer.playbackStateChanged.connect(self.onAudioStateChanged)

        self.defaultInfoLabel = QLabel(self)
        self.defaultInfoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.defaultInfoLabel.setStyleSheet("font-size: 14px; color: #666;")

        self.addWidget(self.textEdit)
        self.addWidget(self.imageContainer)
        self.addWidget(self.audioContainer)
        self.addWidget(self.videoWidget)
        self.addWidget(self.defaultInfoLabel)

    def toggleAudioPlayState(self):
        if self.mediaPlayer.playbackState() == self.mediaPlayer.PlaybackState.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def onAudioStateChanged(self, state):
        self.mediaPlayBar.playButton.setPlay(state == self.mediaPlayer.PlaybackState.PlayingState)

    def onAudioPositionChanged(self, position):
        self.mediaPlayBar.progressSlider.setValue(position)
        try:
            self.mediaPlayBar.updateTime(position, self.mediaPlayer.duration())
        except AttributeError:
            pass 

    def onAudioDurationChanged(self, duration):
        self.mediaPlayBar.progressSlider.setRange(0, duration)
        try:
            self.mediaPlayBar.updateTime(self.mediaPlayer.position(), duration)
        except AttributeError:
            pass

    def onSliderValueChanged(self, value):
        if self.mediaPlayer.position() != value:
            self.mediaPlayer.setPosition(value)

    def updateFile(self, path: str):
        self.mediaPlayer.stop()
        self.videoWidget.pause()

        if not os.path.exists(path):
            self.defaultInfoLabel.setText("File not found.")
            self.setCurrentIndex(4)
            return

        if os.path.isdir(path):
            self.showDefaultInfo(path)
            return

        ext = os.path.splitext(path)[1].lower()

        if ext in ['.txt', '.py', '.json', '.md', '.xml', '.log', '.c', '.cpp', '.h', '.java', '.js', '.html', '.css', '.ini', '.sh', '.bat']:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.textEdit.setText(content)
                self.setCurrentIndex(0)
            except Exception:
                self.showDefaultInfo(path)

        elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.ico', '.svg']:
            self.imageLabel.setImage(path)
            self.imageLabel.setScaledSize(QSize(600, 450))
            self.setCurrentIndex(1)

        elif ext in ['.mp3', '.wav', '.ogg', '.flac', '.m4a']:
            self.mediaPlayer.setSource(QUrl.fromLocalFile(path))
            self.setCurrentIndex(2)
            self.mediaPlayer.play()

        elif ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv']:
            self.videoWidget.setVideo(QUrl.fromLocalFile(path))
            self.setCurrentIndex(3)
            self.videoWidget.play()

        else:
            self.showDefaultInfo(path)

    def showDefaultInfo(self, path):
        try:
            size = os.path.getsize(path)
            ctime = os.path.getctime(path)
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ctime))
            info = f"Path: {path}\nSize: {size} bytes\nCreated: {time_str}"
        except Exception:
            info = f"Path: {path}"

        self.defaultInfoLabel.setText(info)
        self.setCurrentIndex(4)