from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from qfluentwidgets import ScrollArea, SettingCardGroup, SettingCard, LineEdit, PasswordLineEdit, PrimaryPushButton
from qfluentwidgets import FluentIcon as FIF
from app.common.config import cfg

class SettingInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("settingInterface")
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("background-color: transparent;")
        
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        self.setWidget(self.scrollWidget)
        self.scrollWidget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)
        
        self.apiGroup = SettingCardGroup("接口设置", self.scrollWidget)

        self.baseUrlCard = SettingCard(
            FIF.LINK,
            "Base URL",
            "接口基础地址",
            self.apiGroup
        )
        self.baseUrlEdit = LineEdit(self.baseUrlCard)
        self.baseUrlEdit.setText(str(cfg.base_url.value))
        self.baseUrlCard.hBoxLayout.addWidget(self.baseUrlEdit)

        self.apiKeyCard = SettingCard(
            FIF.FINGERPRINT,
            "API Key",
            "访问接口的密钥",
            self.apiGroup
        )
        self.apiKeyEdit = PasswordLineEdit(self.apiKeyCard)
        self.apiKeyEdit.setText(str(cfg.api_key.value))
        self.apiKeyCard.hBoxLayout.addWidget(self.apiKeyEdit)

        self.modelNameCard = SettingCard(
            FIF.ROBOT,
            "模型名称",
            "调用的模型名称",
            self.apiGroup
        )
        self.modelNameEdit = LineEdit(self.modelNameCard)
        self.modelNameEdit.setText(str(cfg.model_name.value))
        self.modelNameCard.hBoxLayout.addWidget(self.modelNameEdit)

        self.apiGroup.addSettingCard(self.baseUrlCard)
        self.apiGroup.addSettingCard(self.apiKeyCard)
        self.apiGroup.addSettingCard(self.modelNameCard)

        self.saveButton = PrimaryPushButton("保存设置", self.scrollWidget)
        self.saveButton.clicked.connect(self.saveSettings)

        self.vBoxLayout.addWidget(self.apiGroup)
        self.vBoxLayout.addWidget(self.saveButton)
        self.vBoxLayout.addStretch(1)

    def saveSettings(self):
        cfg.set(cfg.base_url, self.baseUrlEdit.text())
        cfg.set(cfg.api_key, self.apiKeyEdit.text())
        cfg.set(cfg.model_name, self.modelNameEdit.text())
