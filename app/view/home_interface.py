import qfluentwidgets as qfw
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QGridLayout, QButtonGroup

from qfluentwidgets import (LineEdit, PrimaryPushButton, PushButton, ComboBox, RadioButton, 
                            FluentIcon as FIF, IconWidget)

class BaseSubPage(QWidget):
    
    nextSignal = pyqtSignal()
    prevSignal = pyqtSignal()

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title = title
        
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(20)

        self.titleLabel = qfw.TitleLabel(self.title, self)
        self.vBoxLayout.addWidget(self.titleLabel)

        self.contentLayout = QVBoxLayout()
        self.vBoxLayout.addLayout(self.contentLayout)
        
        self.vBoxLayout.addStretch(1)

        self.buttonLayout = QHBoxLayout()
        self.prevBtn = PushButton("上一步", self)
        self.nextBtn = PrimaryPushButton("下一步", self)
        
        self.prevBtn.clicked.connect(self.prevSignal)
        self.nextBtn.clicked.connect(self.nextSignal)
        
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.prevBtn)
        self.buttonLayout.addWidget(self.nextBtn)
        
        self.vBoxLayout.addLayout(self.buttonLayout)

class IdentityCard(qfw.ElevatedCardWidget):
    
    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.setClickEnabled(True)
        self.setFixedSize(280, 200)
        
        self.vLayout = QVBoxLayout(self)
        self.vLayout.setSpacing(10)
        self.vLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.iconWidget = IconWidget(icon, self)
        self.iconWidget.setFixedSize(48, 48)
        
        self.titleLabel = qfw.SubtitleLabel(title, self)
        self.contentLabel = qfw.BodyLabel(content, self)
        self.contentLabel.setTextColor(Qt.GlobalColor.gray, Qt.GlobalColor.gray)

        self.vLayout.addWidget(self.iconWidget, 0, Qt.AlignmentFlag.AlignCenter)
        self.vLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignCenter)
        self.vLayout.addWidget(self.contentLabel, 0, Qt.AlignmentFlag.AlignCenter)

class IdentitySelectionInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__("选择办理身份", parent)
        
        self.cardLayout = QHBoxLayout()
        self.cardLayout.setSpacing(20)
        self.cardLayout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        self.applicantCard = IdentityCard(FIF.PEOPLE, "我是申请人", "办理本人的软件著作权登记", self)
        self.agentCard = IdentityCard(FIF.MARKET, "我是代理人", "受他人委托办理软件著作权登记", self)
        
        self.cardLayout.addWidget(self.applicantCard)
        self.cardLayout.addWidget(self.agentCard)
        self.cardLayout.addStretch(1)
        
        self.contentLayout.addLayout(self.cardLayout)
        
        self.applicantCard.clicked.connect(self.nextSignal)
        
        self.prevBtn.hide()

class SoftwareAppInfoInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__("软件申请信息", parent)
        
        self.formLayout = QGridLayout()
        self.formLayout.setVerticalSpacing(20)
        self.formLayout.setHorizontalSpacing(10)
        
        self.acquisitionLabel = qfw.BodyLabel("权利取得方式", self)
        self.acquisitionGroup = QButtonGroup(self)
        self.originalRadio = RadioButton("原始取得", self)
        self.derivedRadio = RadioButton("继受取得", self)
        self.acquisitionGroup.addButton(self.originalRadio)
        self.acquisitionGroup.addButton(self.derivedRadio)
        self.originalRadio.setChecked(True)
        
        radioLayout = QHBoxLayout()
        radioLayout.addWidget(self.originalRadio)
        radioLayout.addWidget(self.derivedRadio)
        radioLayout.addStretch(1)
        
        self.formLayout.addWidget(self.acquisitionLabel, 0, 0)
        self.formLayout.addLayout(radioLayout, 0, 1)

        self.fullNameLabel = qfw.BodyLabel("软件全称", self)
        self.fullNameEdit = LineEdit(self)
        self.fullNameEdit.setPlaceholderText("请输入软件全称")
        self.fullNameEdit.setFixedWidth(400)
        self.formLayout.addWidget(self.fullNameLabel, 1, 0)
        self.formLayout.addWidget(self.fullNameEdit, 1, 1)

        self.abbrLabel = qfw.BodyLabel("软件简称", self)
        self.abbrEdit = LineEdit(self)
        self.abbrEdit.setPlaceholderText("请输入软件简称，如无简称请留空，不要填写“无”")
        self.abbrEdit.setFixedWidth(400)
        self.formLayout.addWidget(self.abbrLabel, 2, 0)
        self.formLayout.addWidget(self.abbrEdit, 2, 1)

        self.versionLabel = qfw.BodyLabel("版本号", self)
        self.versionEdit = LineEdit(self)
        self.versionEdit.setPlaceholderText("请输入版本号")
        self.versionEdit.setFixedWidth(400)
        self.formLayout.addWidget(self.versionLabel, 3, 0)
        self.formLayout.addWidget(self.versionEdit, 3, 1)

        self.scopeLabel = qfw.BodyLabel("权利范围", self)
        self.scopeCombo = ComboBox(self)
        self.scopeCombo.addItems(["全部权利", "部分权利"])
        self.scopeCombo.setFixedWidth(200)
        self.formLayout.addWidget(self.scopeLabel, 4, 0)
        self.formLayout.addWidget(self.scopeCombo, 4, 1)
        
        self.contentLayout.addLayout(self.formLayout)

class SoftwareDevInfoInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__("软件开发信息", parent)
        self.contentLayout.addWidget(qfw.SubtitleLabel("此处填写软件开发信息", self))

class SoftwareFeaturesInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__("软件功能与特点", parent)
        self.contentLayout.addWidget(qfw.SubtitleLabel("此处填写软件功能与特点", self))

class ConfirmationInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__("确认信息", parent)
        self.contentLayout.addWidget(qfw.SubtitleLabel("请确认填报信息", self))

class CompletionInterface(BaseSubPage):

    def __init__(self, parent=None):
        super().__init__("填报完成", parent)
        self.contentLayout.addWidget(qfw.SubtitleLabel("填报已完成", self))

class HomeInterface(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("homeInterface")
        
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 20)
        self.vBoxLayout.setSpacing(20)

        self.breadcrumb = qfw.BreadcrumbBar(self)
        self.breadcrumb.setSpacing(20)

        self.vBoxLayout.addWidget(self.breadcrumb)

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

        qfw.setFont(self.breadcrumb, 20)

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
