import qfluentwidgets as qfw
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPainter, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QGridLayout, QButtonGroup


class BaseSubPage(QWidget):
    
    nextSignal = pyqtSignal()
    prevSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._parent = parent
        self.backgroundPixmap = QPixmap("./resources/background.png")
        
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(20)

        self.contentLayout = QVBoxLayout()
        self.vBoxLayout.addLayout(self.contentLayout)
        
        self.vBoxLayout.addStretch(1)

        self.buttonLayout = QHBoxLayout()
        self.prevBtn = qfw.PushButton("上一步", self)
        self.nextBtn = qfw.PrimaryPushButton("下一步", self)
        
        self.prevBtn.clicked.connect(self.prevSignal)
        self.nextBtn.clicked.connect(self.nextSignal)
        
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.prevBtn)
        self.buttonLayout.addWidget(self.nextBtn)
        
        self.vBoxLayout.addLayout(self.buttonLayout)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.setOpacity(0.05)
        
        pixmap = self.backgroundPixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        x = int((self.width() - pixmap.width()) / 2)
        y = int((self.height() - pixmap.height()) / 2)
        painter.drawPixmap(x, y, pixmap)

class IdentityCard(qfw.ElevatedCardWidget):
    
    def __init__(self, icon, title, content, parent=None):
        self._parent = parent
        super().__init__(parent)
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
        
        self.prevBtn.hide()
        self.nextBtn.hide()

class SoftwareAppInfoInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.group = qfw.SettingCardGroup("软件申请信息", self)
        
        self.acquisitionCard = qfw.SettingCard(
            qfw.FluentIcon.CERTIFICATE,
            "权利取得方式",
            "请选择软件权利的取得方式",
            self.group
        )
        self.acquisitionGroup = QButtonGroup(self)
        self.originalRadio = qfw.RadioButton("原始取得", self.acquisitionCard)
        self.derivedRadio = qfw.RadioButton("继受取得", self.acquisitionCard)
        self.acquisitionGroup.addButton(self.originalRadio)
        self.acquisitionGroup.addButton(self.derivedRadio)
        self.originalRadio.setChecked(True)
        
        self.acquisitionCard.hBoxLayout.addWidget(self.originalRadio)
        self.acquisitionCard.hBoxLayout.addSpacing(20)
        self.acquisitionCard.hBoxLayout.addWidget(self.derivedRadio)
        self.acquisitionCard.hBoxLayout.addSpacing(20)

        self.fullNameCard = qfw.SettingCard(
            qfw.FluentIcon.EDIT,
            "软件全称",
            "请输入软件的全称",
            self.group
        )
        self.fullNameEdit = qfw.LineEdit(self.fullNameCard)
        self.fullNameEdit.setPlaceholderText("请输入软件全称")
        self.fullNameEdit.setFixedWidth(300)
        self.fullNameCard.hBoxLayout.addWidget(self.fullNameEdit)
        self.fullNameCard.hBoxLayout.addSpacing(20)

        self.abbrCard = qfw.SettingCard(
            qfw.FluentIcon.TAG,
            "软件简称",
            "请输入软件简称（选填）",
            self.group
        )
        self.abbrEdit = qfw.LineEdit(self.abbrCard)
        self.abbrEdit.setPlaceholderText("如有简称请填写")
        self.abbrEdit.setFixedWidth(300)
        self.abbrCard.hBoxLayout.addWidget(self.abbrEdit)
        self.abbrCard.hBoxLayout.addSpacing(20)

        self.versionCard = qfw.SettingCard(
            qfw.FluentIcon.INFO,
            "版本号",
            "请输入软件版本号",
            self.group
        )
        self.versionEdit = qfw.LineEdit(self.versionCard)
        self.versionEdit.setPlaceholderText("V1.0")
        self.versionEdit.setFixedWidth(300)
        self.versionCard.hBoxLayout.addWidget(self.versionEdit)
        self.versionCard.hBoxLayout.addSpacing(20)

        self.scopeCard = qfw.SettingCard(
            qfw.FluentIcon.VIEW,
            "权利范围",
            "请选择权利范围",
            self.group
        )
        self.scopeCombo = qfw.ComboBox(self.scopeCard)
        self.scopeCombo.addItems(["全部权利", "部分权利"])
        self.scopeCombo.setFixedWidth(200)
        self.scopeCard.hBoxLayout.addWidget(self.scopeCombo)
        self.scopeCard.hBoxLayout.addSpacing(20)
        
        self.group.addSettingCard(self.acquisitionCard)
        self.group.addSettingCard(self.fullNameCard)
        self.group.addSettingCard(self.abbrCard)
        self.group.addSettingCard(self.versionCard)
        self.group.addSettingCard(self.scopeCard)
        
        self.contentLayout.addWidget(self.group)

class SoftwareDevInfoInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.contentLayout.addWidget(qfw.SubtitleLabel("此处填写软件开发信息", self))

class SoftwareFeaturesInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.contentLayout.addWidget(qfw.SubtitleLabel("此处填写软件功能与特点", self))

class ConfirmationInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.contentLayout.addWidget(qfw.SubtitleLabel("请确认填报信息", self))

class CompletionInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.contentLayout.addWidget(qfw.SubtitleLabel("填报已完成", self))

class HomeInterface(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.setObjectName("homeInterface")
        
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 20)
        self.vBoxLayout.setSpacing(20)

        self.breadcrumb = qfw.BreadcrumbBar(self)
        self.breadcrumb.setSpacing(16)
        qfw.setFont(self.breadcrumb, 20, QFont.Weight.Bold)

        self.breadcrumbLayout = QHBoxLayout()
        self.breadcrumbLayout.setContentsMargins(10, 0, 0, 0)
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
