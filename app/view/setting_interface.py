import qfluentwidgets as qfw
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from app.common.config import cfg


class SettingInterface(qfw.ScrollArea):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self._parent = parent
        self.setWidgetResizable(True)
        self.setObjectName("settingInterface")
        self.setStyleSheet("background-color: transparent;")
        
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        self.vBoxLayout.setSpacing(20)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 20)
        self.setWidget(self.scrollWidget)
        
        self.apiGroup = qfw.SettingCardGroup("接口设置", self.scrollWidget)

        self.baseUrlCard = qfw.SettingCard(
            qfw.FluentIcon.LINK,
            "Base URL",
            "接口基础地址",
            self.apiGroup
        )
        self.baseUrlEdit = qfw.LineEdit(self.baseUrlCard)
        self.baseUrlEdit.setText(str(cfg.base_url.value))
        self.baseUrlEdit.setFixedWidth(200)
        self.baseUrlCard.hBoxLayout.addWidget(self.baseUrlEdit)
        self.baseUrlCard.hBoxLayout.addSpacing(16)

        self.modelNameCard = qfw.SettingCard(
            qfw.FluentIcon.ROBOT,
            "Model Name",
            "调用的模型名称",
            self.apiGroup
        )
        self.modelNameEdit = qfw.LineEdit(self.modelNameCard)
        self.modelNameEdit.setText(str(cfg.model_name.value))
        self.modelNameEdit.setFixedWidth(200)
        self.modelNameCard.hBoxLayout.addWidget(self.modelNameEdit)
        self.modelNameCard.hBoxLayout.addSpacing(16)

        self.apiKeyCard = qfw.SettingCard(
            qfw.FluentIcon.FINGERPRINT, 
            "API Key",
            "访问接口的密钥",
            self.apiGroup
        )
        self.apiKeyEdit = qfw.PasswordLineEdit(self.apiKeyCard)
        self.apiKeyEdit.setText(str(cfg.api_key.value))
        self.apiKeyEdit.setFixedWidth(200)
        self.apiKeyCard.hBoxLayout.addWidget(self.apiKeyEdit)
        self.apiKeyCard.hBoxLayout.addSpacing(16)

        self.__connectSignalToSlot()

        self.apiGroup.addSettingCard(self.baseUrlCard)
        self.apiGroup.addSettingCard(self.modelNameCard)
        self.apiGroup.addSettingCard(self.apiKeyCard)

        self.vBoxLayout.addWidget(self.apiGroup)

        self.personalGroup = qfw.SettingCardGroup("个性化", self.scrollWidget)
        
        self.themeCard = qfw.OptionsSettingCard(
            cfg.theme,
            qfw.FluentIcon.BRUSH,
            "应用主题",
            "调整应用的外观颜色",
            texts=["浅色", "深色", "跟随系统"],
            parent=self.personalGroup
        )
        self.themeCard.optionChanged.connect(lambda: qfw.setTheme(cfg.theme.value))
        self.personalGroup.addSettingCard(self.themeCard)
        self.vBoxLayout.addWidget(self.personalGroup)

        self.hyperlinkGroup = qfw.SettingCardGroup("快捷方式", self.scrollWidget)

        hyperlink_1 = qfw.HyperlinkCard(
            url="https://register.ccopyright.com.cn/registration.html",
            text="申请软件著作权",
            icon=qfw.FluentIcon.HELP,
            title="中国版权登记业务平台",
            content="申请与提交软件著作权"
        )

        hyperlink_2 = qfw.HyperlinkCard(
            url="https://platform.iflow.cn",
            text="获取API密钥",
            icon=qfw.FluentIcon.VPN,
            title="心流开放平台",
            content="获取API密钥"
        )
        
        self.hyperlinkGroup.addSettingCard(hyperlink_1)
        self.hyperlinkGroup.addSettingCard(hyperlink_2)
        self.vBoxLayout.addWidget(self.hyperlinkGroup)

        self.vBoxLayout.addStretch(1)

    def __connectSignalToSlot(self) -> None:
        self.baseUrlEdit.editingFinished.connect(self.__saveApiConfig)
        self.modelNameEdit.editingFinished.connect(self.__saveApiConfig)
        self.apiKeyEdit.editingFinished.connect(self.__saveApiConfig)

    def __saveApiConfig(self) -> None:
        cfg.set(cfg.base_url, self.baseUrlEdit.text())
        cfg.set(cfg.model_name, self.modelNameEdit.text())
        cfg.set(cfg.api_key, self.apiKeyEdit.text())
        cfg.save()
