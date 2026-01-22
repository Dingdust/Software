import qfluentwidgets as qfw
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPainter, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QButtonGroup


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
        self.scrollArea.setWidget(self.scrollWidget)
        
        self.vBoxLayout.addWidget(self.scrollArea)

        self.buttonLayout = QHBoxLayout()
        self.prevBtn = qfw.PushButton("上一步", self)
        self.nextBtn = qfw.PrimaryPushButton("下一步", self)
        
        self.prevBtn.clicked.connect(self.prevSignal)
        self.nextBtn.clicked.connect(self.nextSignal)
        
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.prevBtn)
        self.buttonLayout.addWidget(self.nextBtn)
        
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

class IdentitySelectionInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        
        self.cardLayout = QHBoxLayout()
        self.cardLayout.setSpacing(64)
        self.cardLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        self.applicantCard = IdentityCard(qfw.FluentIcon.PEOPLE, "我是申请人", "办理本人的软件著作权登记", self)
        self.agentCard = IdentityCard(qfw.FluentIcon.MARKET, "我是代理人", "受他人委托办理软件著作权登记", self)
        
        self.cardLayout.addWidget(self.applicantCard)
        self.cardLayout.addWidget(self.agentCard)
        self.cardLayout.addStretch(1)
        
        self.contentLayout.addLayout(self.cardLayout)
        
        self.applicantCard.clicked.connect(self.nextSignal)
        self.agentCard.clicked.connect(self.show_info)
        
        self.prevBtn.hide()
        self.nextBtn.hide()

class SoftwareAppInfoInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        
        self.acquisitionCard = qfw.SettingCard(
            qfw.FluentIcon.CERTIFICATE,
            "权利取得方式",
            "请选择软件权利的取得方式",
            self.scrollWidget
        )
        self.acquisitionGroup = QButtonGroup(self)
        self.originalRadio = qfw.RadioButton("原始取得", self.acquisitionCard)
        self.derivedRadio = qfw.RadioButton("继受取得", self.acquisitionCard)
        self.acquisitionGroup.addButton(self.originalRadio)
        self.acquisitionGroup.addButton(self.derivedRadio)
        self.originalRadio.setChecked(True)
        self.derivedRadio.clicked.connect(self.onDerivedClicked)
        
        self.acquisitionCard.hBoxLayout.addWidget(self.originalRadio)
        self.acquisitionCard.hBoxLayout.addSpacing(20)
        self.acquisitionCard.hBoxLayout.addWidget(self.derivedRadio)
        self.acquisitionCard.hBoxLayout.addSpacing(20)

        self.fullNameCard = qfw.SettingCard(
            qfw.FluentIcon.EDIT,
            "软件全称",
            "请输入软件的全称",
            self.scrollWidget
        )
        self.fullNameEdit = qfw.LineEdit(self.fullNameCard)
        self.fullNameEdit.setPlaceholderText("请输入软件全称")
        self.fullNameEdit.setFixedWidth(360)
        self.fullNameCard.hBoxLayout.addWidget(self.fullNameEdit)
        self.fullNameCard.hBoxLayout.addSpacing(20)

        self.abbrCard = qfw.SettingCard(
            qfw.FluentIcon.TAG,
            "软件简称",
            "请输入软件简称（选填）",
            self.scrollWidget
        )
        self.abbrEdit = qfw.LineEdit(self.abbrCard)
        self.abbrEdit.setPlaceholderText("请输入软件简称，如无简称请留空，不要填写“无”。")
        self.abbrEdit.setFixedWidth(360)
        self.abbrCard.hBoxLayout.addWidget(self.abbrEdit)
        self.abbrCard.hBoxLayout.addSpacing(20)

        self.versionCard = qfw.SettingCard(
            qfw.FluentIcon.INFO,
            "版本号",
            "请输入软件版本号",
            self.scrollWidget
        )
        self.versionEdit = qfw.LineEdit(self.versionCard)
        self.versionEdit.setPlaceholderText("请输入版本号")
        self.versionEdit.setFixedWidth(360)
        self.versionCard.hBoxLayout.addWidget(self.versionEdit)
        self.versionCard.hBoxLayout.addSpacing(20)

        self.scopeCard = qfw.SettingCard(
            qfw.FluentIcon.VIEW,
            "权利范围",
            "请选择权利范围",
            self.scrollWidget
        )
        self.scopeGroup = QButtonGroup(self)
        self.allRightsRadio = qfw.RadioButton("全部权利", self.scopeCard)
        self.partRightsRadio = qfw.RadioButton("部分权利", self.scopeCard)
        self.scopeGroup.addButton(self.allRightsRadio)
        self.scopeGroup.addButton(self.partRightsRadio)
        self.allRightsRadio.setChecked(True)
        self.partRightsRadio.clicked.connect(self.onPartClicked)
        
        self.scopeCard.hBoxLayout.addWidget(self.allRightsRadio)
        self.scopeCard.hBoxLayout.addSpacing(20)
        self.scopeCard.hBoxLayout.addWidget(self.partRightsRadio)
        self.scopeCard.hBoxLayout.addSpacing(20)
        
        self.contentLayout.addWidget(self.acquisitionCard)
        self.contentLayout.addWidget(self.fullNameCard)
        self.contentLayout.addWidget(self.abbrCard)
        self.contentLayout.addWidget(self.versionCard)
        self.contentLayout.addWidget(self.scopeCard)

        self.nextBtn.disconnect()
        self.nextBtn.clicked.connect(self.check_for_next)

    def onDerivedClicked(self):
        self.show_info()
        QTimer.singleShot(1000, lambda: self.originalRadio.setChecked(True))

    def onPartClicked(self):
        self.show_info()
        QTimer.singleShot(1000, lambda: self.allRightsRadio.setChecked(True))

    def check_for_next(self):
        if self.originalRadio.isChecked():
            if self.fullNameEdit.text() != "":
                if len(self.abbrEdit.text()) <= len(self.fullNameEdit.text()):
                    if self.versionEdit.text() != "":
                        if self.allRightsRadio.isChecked():
                            self.nextSignal.emit()
                        else:
                            self.show_error(content="请检查【权利范围】是否填写正确！")
                    else:
                        self.show_info(content="【版本号】已自动补全，请检查！")
                        self.versionEdit.setText("V1.0")
                        self.versionEdit.setFocus()
                else:
                    self.show_warning(content="软件简称字数多于软件全称，可能发生补正！")
                    self.abbrEdit.setFocus()
            else:
                self.show_error(content="请检查【软件全称】是否填写正确！")
                self.fullNameEdit.setFocus()
        else:
            self.show_error(content="请检查【权利取得方式】是否填写正确！")

class SoftwareDevInfoInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        
        self.acquisitionCard = qfw.SettingCard(
            qfw.FluentIcon.CERTIFICATE,
            "权利取得方式",
            "请选择软件权利的取得方式",
            self.scrollWidget
        )
        self.acquisitionGroup = QButtonGroup(self)
        self.originalRadio = qfw.RadioButton("原始取得", self.acquisitionCard)
        self.derivedRadio = qfw.RadioButton("继受取得", self.acquisitionCard)
        self.acquisitionGroup.addButton(self.originalRadio)
        self.acquisitionGroup.addButton(self.derivedRadio)
        self.originalRadio.setChecked(True)
        self.derivedRadio.clicked.connect(self.onDerivedClicked)
        
        self.acquisitionCard.hBoxLayout.addWidget(self.originalRadio)
        self.acquisitionCard.hBoxLayout.addSpacing(20)
        self.acquisitionCard.hBoxLayout.addWidget(self.derivedRadio)
        self.acquisitionCard.hBoxLayout.addSpacing(20)

        self.fullNameCard = qfw.SettingCard(
            qfw.FluentIcon.EDIT,
            "软件全称",
            "请输入软件的全称",
            self.scrollWidget
        )
        self.fullNameEdit = qfw.LineEdit(self.fullNameCard)
        self.fullNameEdit.setPlaceholderText("请输入软件全称")
        self.fullNameEdit.setFixedWidth(360)
        self.fullNameCard.hBoxLayout.addWidget(self.fullNameEdit)
        self.fullNameCard.hBoxLayout.addSpacing(20)

        self.abbrCard = qfw.SettingCard(
            qfw.FluentIcon.TAG,
            "软件简称",
            "请输入软件简称（选填）",
            self.scrollWidget
        )
        self.abbrEdit = qfw.LineEdit(self.abbrCard)
        self.abbrEdit.setPlaceholderText("请输入软件简称，如无简称请留空，不要填写“无”。")
        self.abbrEdit.setFixedWidth(360)
        self.abbrCard.hBoxLayout.addWidget(self.abbrEdit)
        self.abbrCard.hBoxLayout.addSpacing(20)

        self.versionCard = qfw.SettingCard(
            qfw.FluentIcon.INFO,
            "版本号",
            "请输入软件版本号",
            self.scrollWidget
        )
        self.versionEdit = qfw.LineEdit(self.versionCard)
        self.versionEdit.setPlaceholderText("请输入版本号")
        self.versionEdit.setFixedWidth(360)
        self.versionCard.hBoxLayout.addWidget(self.versionEdit)
        self.versionCard.hBoxLayout.addSpacing(20)

        self.scopeCard = qfw.SettingCard(
            qfw.FluentIcon.VIEW,
            "权利范围",
            "请选择权利范围",
            self.scrollWidget
        )
        self.scopeGroup = QButtonGroup(self)
        self.allRightsRadio = qfw.RadioButton("全部权利", self.scopeCard)
        self.partRightsRadio = qfw.RadioButton("部分权利", self.scopeCard)
        self.scopeGroup.addButton(self.allRightsRadio)
        self.scopeGroup.addButton(self.partRightsRadio)
        self.allRightsRadio.setChecked(True)
        self.partRightsRadio.clicked.connect(self.onPartClicked)
        
        self.scopeCard.hBoxLayout.addWidget(self.allRightsRadio)
        self.scopeCard.hBoxLayout.addSpacing(20)
        self.scopeCard.hBoxLayout.addWidget(self.partRightsRadio)
        self.scopeCard.hBoxLayout.addSpacing(20)
        
        self.contentLayout.addWidget(self.acquisitionCard)
        self.contentLayout.addWidget(self.fullNameCard)
        self.contentLayout.addWidget(self.abbrCard)
        self.contentLayout.addWidget(self.versionCard)
        self.contentLayout.addWidget(self.scopeCard)

        self.nextBtn.disconnect()
        self.nextBtn.clicked.connect(self.check_for_next)

    def onDerivedClicked(self):
        self.show_info()
        QTimer.singleShot(1000, lambda: self.originalRadio.setChecked(True))

    def onPartClicked(self):
        self.show_info()
        QTimer.singleShot(1000, lambda: self.allRightsRadio.setChecked(True))

    def check_for_next(self):
        if self.originalRadio.isChecked():
            if self.fullNameEdit.text() != "":
                if len(self.abbrEdit.text()) <= len(self.fullNameEdit.text()):
                    if self.versionEdit.text() != "":
                        if self.allRightsRadio.isChecked():
                            self.nextSignal.emit()
                        else:
                            self.show_error(content="请检查【权利范围】是否填写正确！")
                    else:
                        self.show_info(content="【版本号】已自动补全，请检查！")
                        self.versionEdit.setText("V1.0")
                        self.versionEdit.setFocus()
                else:
                    self.show_warning(content="软件简称字数多于软件全称，可能发生补正！")
                    self.abbrEdit.setFocus()
            else:
                self.show_error(content="请检查【软件全称】是否填写正确！")
                self.fullNameEdit.setFocus()
        else:
            self.show_error(content="请检查【权利取得方式】是否填写正确！")

class SoftwareFeaturesInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.contentLayout.addWidget(qfw.SubtitleLabel("此处填写软件功能与特点", self))

class ConfirmationInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.contentLayout.addWidget(qfw.SubtitleLabel("请确认填报信息", self))

class CompletionInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.contentLayout.addWidget(qfw.SubtitleLabel("填报已完成", self))

class HomeInterface(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.setObjectName("homeInterface")
        
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(36, 36, 36, 36)

        self.breadcrumb = qfw.BreadcrumbBar(self)
        self.breadcrumb.setSpacing(18)
        qfw.setFont(self.breadcrumb, 18, QFont.Weight.Bold)

        self.breadcrumbLayout = QHBoxLayout()
        self.breadcrumbLayout.setContentsMargins(18, 0, 0, 0)
        self.breadcrumbLayout.addWidget(self.breadcrumb)
        self.vBoxLayout.addLayout(self.breadcrumbLayout)

        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout.addWidget(self.stackedWidget)

        self.pages_info = [
            ("identity", "选择办理身份", IdentitySelectionInterface),
            ("app_info", "软件申请信息", SoftwareAppInfoInterface),
            ("dev_info", "软件开发信息", SoftwareDevInfoInterface),
            ("features", "软件功能与特点", SoftwareFeaturesInterface),
            ("confirm", "确认信息", ConfirmationInterface),
            ("complete", "填报完成", CompletionInterface)
        ]

        self.added_keys = []
        self.route_keys = []
        
        for key, name, cls in self.pages_info:
            page = cls(self)
            page.nextSignal.connect(self.nextPage)
            page.prevSignal.connect(self.prevPage)
            if key == "complete":
                page.nextBtn.hide()

            self.stackedWidget.addWidget(page)
            self.route_keys.append(key)

            if key == "identity":
                self.added_keys.append(key)
                self.breadcrumb.addItem(key, name)

        self.breadcrumb.currentItemChanged.connect(self.switchToPage)

    def switchToPage(self, routeKey):
        if routeKey in self.route_keys:
            index = self.route_keys.index(routeKey)
            self.added_keys = self.route_keys[:index+1]
            self.stackedWidget.setCurrentIndex(index)

    def nextPage(self):
        current_idx = self.stackedWidget.currentIndex()
        if current_idx < self.stackedWidget.count() - 1:
            next_idx = current_idx + 1
            key, name, _ = self.pages_info[next_idx]
            if key not in self.added_keys:
                self.added_keys.append(key)
                self.breadcrumb.addItem(key, name)
            self.breadcrumb.setCurrentItem(key)
            self.stackedWidget.setCurrentIndex(next_idx)

    def prevPage(self):
        current_idx = self.stackedWidget.currentIndex()
        if current_idx > 0:
            prev_idx = current_idx - 1
            key = self.route_keys[prev_idx]
            self.breadcrumb.setCurrentItem(key)
            self.stackedWidget.setCurrentIndex(prev_idx)
