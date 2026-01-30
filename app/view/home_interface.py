import qfluentwidgets as qfw
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QButtonGroup, QLabel

import app.view.custom_widget as custom


class IdentitySelectionInterface(custom.BaseSubPage):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._parent = parent
        
        self.cardLayout = QHBoxLayout()
        self.cardLayout.setSpacing(64)
        self.cardLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.applicantCard = custom.IdentityCard(qfw.FluentIcon.PEOPLE, "我是申请人", "办理本人的软件著作权登记", self)
        self.agentCard = custom.IdentityCard(qfw.FluentIcon.MARKET, "我是代理人", "受他人委托办理软件著作权登记", self)
        
        self.cardLayout.addWidget(self.applicantCard)
        self.cardLayout.addWidget(self.agentCard)
        self.cardLayout.addStretch(1)
        
        self.contentLayout.addLayout(self.cardLayout)
        
        self.applicantCard.clicked.connect(self.nextSignal)
        self.agentCard.clicked.connect(self.show_info)
        
        self.prevBtn.hide()
        self.nextBtn.hide()


class SoftwareAppInfoInterface(custom.BaseSubPage):

    def __init__(self, parent=None) -> None:
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

        self.nextBtn.clicked.disconnect()
        self.nextBtn.clicked.connect(self.check_for_next)

    def onDerivedClicked(self) -> None:
        self.show_info()
        QTimer.singleShot(1000, lambda: self.originalRadio.setChecked(True))

    def onPartClicked(self) -> None:
        self.show_info()
        QTimer.singleShot(1000, lambda: self.allRightsRadio.setChecked(True))

    def check_for_next(self) -> None:
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


class SoftwareDevInfoInterface(custom.BaseSubPage):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._parent = parent
        
        self.classCard = qfw.SettingCard(
            qfw.FluentIcon.DICTIONARY,
            "软件分类",
            "请选择软件分类",
            self.scrollWidget
        )
        self.classGroup = qfw.ComboBox(self)
        self.classGroup.setFixedWidth(160)
        self.classCard.hBoxLayout.addWidget(self.classGroup, 0, Qt.AlignmentFlag.AlignRight)
        self.classCard.hBoxLayout.addSpacing(16)
        self.classItems = ["请选择软件分类", "应用软件", "嵌入式软件", "中间件", "操作系统"]
        self.classGroup.addItems(self.classItems)
        self.classGroup.setPlaceholderText("请选择软件分类")

        self.introCard = qfw.SettingCard(
            qfw.FluentIcon.LABEL,
            "软件说明",
            "请就软件原创性进行选择",
            self.scrollWidget
        )
        self.introGroup = QButtonGroup(self)
        self.originalRadio = qfw.RadioButton("原创", self.introCard)
        self.derivedRadio = qfw.RadioButton("修改（含翻译软件、合成软件）", self.introCard)
        self.introGroup.addButton(self.originalRadio)
        self.introGroup.addButton(self.derivedRadio)
        self.originalRadio.setChecked(True)
        self.derivedRadio.clicked.connect(self.onDerivedClicked)
        
        self.introCard.hBoxLayout.addWidget(self.originalRadio)
        self.introCard.hBoxLayout.addSpacing(20)
        self.introCard.hBoxLayout.addWidget(self.derivedRadio)
        self.introCard.hBoxLayout.addSpacing(20)

        self.devFormCard = qfw.SettingCard(
            qfw.FluentIcon.CODE,
            "开发方式",
            "请选择软件的开发方式",
            self.scrollWidget
        )
        self.devFormGroup = QButtonGroup(self)
        self.singleRadio = qfw.RadioButton("单独开发", self.devFormCard)
        self.coopRadio = qfw.RadioButton("合作开发", self.devFormCard)
        self.delegateRadio = qfw.RadioButton("委托开发", self.devFormCard)
        self.taskRadio = qfw.RadioButton("下达任务开发", self.devFormCard)
        self.devFormGroup.addButton(self.singleRadio)
        self.devFormGroup.addButton(self.coopRadio)
        self.devFormGroup.addButton(self.delegateRadio)
        self.devFormGroup.addButton(self.taskRadio)
        self.singleRadio.setChecked(True)
        self.coopRadio.clicked.connect(self.onUnSupDevFormClicked)
        self.delegateRadio.clicked.connect(self.onUnSupDevFormClicked)
        self.taskRadio.clicked.connect(self.onUnSupDevFormClicked)
        
        self.devFormCard.hBoxLayout.addWidget(self.singleRadio)
        self.devFormCard.hBoxLayout.addSpacing(20)
        self.devFormCard.hBoxLayout.addWidget(self.coopRadio)
        self.devFormCard.hBoxLayout.addSpacing(20)
        self.devFormCard.hBoxLayout.addWidget(self.delegateRadio)
        self.devFormCard.hBoxLayout.addSpacing(20)
        self.devFormCard.hBoxLayout.addWidget(self.taskRadio)
        self.devFormCard.hBoxLayout.addSpacing(20)
        
        self.devFinishCard = qfw.SettingCard(
            qfw.FluentIcon.CALENDAR,
            "开发完成日期",
            "请选择软件的开发完成日期",
            self.scrollWidget
        )
        self.devFinishDate = qfw.FastCalendarPicker(self)
        self.devFinishDate.setFixedWidth(160)
        self.devFinishCard.hBoxLayout.addWidget(self.devFinishDate, 0, Qt.AlignmentFlag.AlignRight)
        self.devFinishCard.hBoxLayout.addSpacing(16)
        self.devFinishDate.setText("请选择日期")

        self.publishCard = qfw.SettingCard(
            qfw.FluentIcon.IMAGE_EXPORT,
            "发表状态",
            "请选择软件的发表状态",
            self.scrollWidget
        )
        self.publishGroup = QButtonGroup(self)
        self.unPublishRadio = qfw.RadioButton("未发表", self.publishCard)
        self.publishRadio = qfw.RadioButton("已发表", self.publishCard)
        self.publishGroup.addButton(self.unPublishRadio)
        self.publishGroup.addButton(self.publishRadio)
        self.unPublishRadio.setChecked(True)
        self.publishRadio.clicked.connect(self.onPublishClicked)
        
        self.publishCard.hBoxLayout.addWidget(self.unPublishRadio)
        self.publishCard.hBoxLayout.addSpacing(20)
        self.publishCard.hBoxLayout.addWidget(self.publishRadio)
        self.publishCard.hBoxLayout.addSpacing(20)

        self.authorCard = qfw.SettingCard(
            qfw.FluentIcon.PEOPLE,
            "著作权人",
            "请核对著作权人信息",
            self.scrollWidget
        )
        self.authorName = qfw.LineEdit(self)
        self.authorName.setFixedWidth(240)
        self.authorCard.hBoxLayout.addWidget(self.authorName, 0, Qt.AlignmentFlag.AlignRight)
        self.authorCard.hBoxLayout.addSpacing(16)
        self.authorName.setText("请前往【用户中心】实名验证")
        self.authorName.setReadOnly(True)
        self.authorName.setEnabled(False)

        self.contentLayout.addWidget(self.classCard)
        self.contentLayout.addWidget(self.introCard)
        self.contentLayout.addWidget(self.devFormCard)
        self.contentLayout.addWidget(self.devFinishCard)
        self.contentLayout.addWidget(self.publishCard)
        self.contentLayout.addWidget(self.authorCard)

        self.nextBtn.clicked.disconnect()
        self.nextBtn.clicked.connect(self.check_for_next)

    def onDerivedClicked(self) -> None:
        self.show_info()
        QTimer.singleShot(1000, lambda: self.originalRadio.setChecked(True))

    def onUnSupDevFormClicked(self) -> None:
        self.show_info()
        QTimer.singleShot(1000, lambda: self.singleRadio.setChecked(True))

    def onPublishClicked(self) -> None:
        self.show_info()
        QTimer.singleShot(1000, lambda: self.unPublishRadio.setChecked(True))

    def check_for_next(self) -> None:
        if self.classGroup.text() in self.classItems[1:]:
            if self.originalRadio.isChecked():
                if self.singleRadio.isChecked():
                    if self.devFinishDate.date.isValid():
                        if self.unPublishRadio.isChecked():
                            self.nextSignal.emit()
                        else:
                            self.show_error(content="请检查【发表状态】是否填写正确！")
                    else:
                        self.show_error(content="请检查【开发完成日期】是否填写正确！")
                        self.devFinishDate.setFocus()
                else:
                    self.show_error(content="请检查【开发方式】是否填写正确！")
            else:
                self.show_error(content="请检查【软件说明】是否填写正确！")
        else:
            self.show_error(content="请检查【软件分类】是否填写正确！")
            self.classGroup.setFocus()


class SoftwareFeaturesInterface(custom.BaseSubPage):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._parent = parent
        
        self.devHardwareEnvCard = custom.EditSettingCard(
            qfw.FluentIcon.SETTING,
            "开发的硬件环境",
            "请填写开发的硬件环境（50字）",
            self.scrollWidget
        )

        self.runHardwareEnvCard = custom.EditSettingCard(
            qfw.FluentIcon.IOT,
            "运行的硬件环境",
            "请填写运行的硬件环境（50字）",
            self.scrollWidget
        )

        self.devOSEnvCard = custom.EditSettingCard(
            qfw.FluentIcon.INFO,
            "开发该软件的操作系统",
            "请填写开发该软件的操作系统（50字）",
            self.scrollWidget
        )

        self.devEnvToolCard = custom.EditSettingCard(
            qfw.FluentIcon.DEVELOPER_TOOLS,
            "软件开发环境 / 开发工具",
            "请填写软件开发环境 / 开发工具（50字）",
            self.scrollWidget
        )

        self.runPlatformOSCard = custom.EditSettingCard(
            qfw.FluentIcon.GLOBE,
            "该软件的运行平台 / 操作系统",
            "请填写该软件的运行平台 / 操作系统（50字）",
            self.scrollWidget
        )

        self.runEnvSoftwareCard = custom.EditSettingCard(
            qfw.FluentIcon.APPLICATION,
            "软件运行支撑环境 / 支持软件",
            "请填写软件运行支撑环境 / 支持软件（50字）",
            self.scrollWidget
        )

        self.devLanguageCard = custom.DevLanguageCard(self.scrollWidget)

        self.codeLineCard = qfw.SettingCard(
            qfw.FluentIcon.CODE,
            "源程序量",
            "请输入源程序量的代码总行数",
            self.scrollWidget
        )
        self.codeLineEdit = qfw.LineEdit(self.codeLineCard)
        self.codeLineEdit.setPlaceholderText("请输入...")
        self.codeLineEdit.setFixedWidth(160)
        self.codeLineCard.hBoxLayout.addWidget(self.codeLineEdit)
        self.codeLineCard.hBoxLayout.addSpacing(24)
        self.codeLineCard.hBoxLayout.addWidget(QLabel("行", self.codeLineCard))
        self.codeLineCard.hBoxLayout.addSpacing(16)

        self.devTargetCard = custom.EditSettingCard(
            qfw.FluentIcon.PIN,
            "开发目的",
            "请填写开发目的（50字）",
            self.scrollWidget
        )

        self.TargetDomainCard = custom.EditSettingCard(
            qfw.FluentIcon.EDIT,
            "面向领域 / 行业",
            "请填写面向领域 / 行业（50字）",
            self.scrollWidget
        )

        self.MainFunctionCard = custom.EditSettingCard(
            qfw.FluentIcon.SEND,
            "软件的主要功能",
            "请填写软件的主要功能（200字）",
            self.scrollWidget
        )

        self.featuresCard = custom.FeaturesCard(self.scrollWidget)

        self.codeIdentifyCard = custom.FileUploadCard(
            qfw.FluentIcon.COMMAND_PROMPT,
            "程序鉴别材料",
            "源程序前连续的30页和后连续的30页",
            self.scrollWidget
            )

        self.documentIdentifyCard = custom.FileUploadCard(
            qfw.FluentIcon.DICTIONARY_ADD,
            "文档鉴别材料",
            "提交任何一种文档的前连续的30页和后连续的30页",
            self.scrollWidget
        )

        self.otherMaterialCard = custom.FileUploadCard(
            qfw.FluentIcon.FOLDER_ADD,
            "其他相关证明文件",
            "请上传其他相关证明文件（选填）",
            self.scrollWidget
        )

        self.contentLayout.addWidget(self.devHardwareEnvCard)
        self.contentLayout.addWidget(self.runHardwareEnvCard)
        self.contentLayout.addWidget(self.devOSEnvCard)
        self.contentLayout.addWidget(self.devEnvToolCard)
        self.contentLayout.addWidget(self.runPlatformOSCard)
        self.contentLayout.addWidget(self.runEnvSoftwareCard)
        self.contentLayout.addWidget(self.devLanguageCard)
        self.contentLayout.addWidget(self.codeLineCard)
        self.contentLayout.addWidget(self.devTargetCard)
        self.contentLayout.addWidget(self.TargetDomainCard)
        self.contentLayout.addWidget(self.MainFunctionCard)
        self.contentLayout.addWidget(self.featuresCard)
        self.contentLayout.addWidget(self.codeIdentifyCard)
        self.contentLayout.addWidget(self.documentIdentifyCard)
        self.contentLayout.addWidget(self.otherMaterialCard)

        self.nextBtn.clicked.disconnect()
        self.nextBtn.clicked.connect(self.check_for_next)

    def check_for_next(self) -> None:
        self.nextSignal.emit()


class ConfirmationInterface(custom.BaseSubPage):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._parent = parent
        self.contentLayout.addWidget(qfw.SubtitleLabel("请确认填报信息", self))


class CompletionInterface(custom.BaseSubPage):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._parent = parent
        self.contentLayout.addWidget(qfw.SubtitleLabel("填报已完成", self))


class HomeInterface(QWidget):
    
    def __init__(self, parent=None) -> None:
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

    def switchToPage(self, routeKey: str) -> None:
        if routeKey in self.route_keys:
            index = self.route_keys.index(routeKey)
            self.added_keys = self.route_keys[:index+1]
            self.stackedWidget.setCurrentIndex(index)

    def nextPage(self) -> None:
        current_idx = self.stackedWidget.currentIndex()
        if current_idx < self.stackedWidget.count() - 1:
            next_idx = current_idx + 1
            key, name, _ = self.pages_info[next_idx]
            if key not in self.added_keys:
                self.added_keys.append(key)
                self.breadcrumb.addItem(key, name)
            self.breadcrumb.setCurrentItem(key)
            self.stackedWidget.setCurrentIndex(next_idx)

    def prevPage(self) -> None:
        current_idx = self.stackedWidget.currentIndex()
        if current_idx > 0:
            prev_idx = current_idx - 1
            key = self.route_keys[prev_idx]
            self.breadcrumb.setCurrentItem(key)
            self.stackedWidget.setCurrentIndex(prev_idx)
