from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from qfluentwidgets import (ScrollArea, SettingCardGroup, SettingCard, LineEdit, PasswordLineEdit, 
                            PrimaryPushButton, OptionsSettingCard, setTheme, Theme)
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
        self.vBoxLayout.setContentsMargins(36, 36, 36, 36)
        self.vBoxLayout.setSpacing(28)
        self.setWidget(self.scrollWidget)
        
        # Personalization Group
        self.personalGroup = SettingCardGroup("个性化", self.scrollWidget)
        
        self.themeCard = OptionsSettingCard(
            cfg.theme,
            FIF.BRUSH,
            "应用主题",
            "调整应用的外观颜色",
            texts=["浅色", "深色", "跟随系统"],
            parent=self.personalGroup
        )
        self.themeCard.optionChanged.connect(lambda ci: setTheme(cfg.theme.value))
        self.personalGroup.addSettingCard(self.themeCard)
        self.vBoxLayout.addWidget(self.personalGroup)
        
        self.apiGroup = SettingCardGroup("接口设置", self.scrollWidget)

        self.baseUrlCard = SettingCard(
            FIF.LINK,
            "Base URL",
            "接口基础地址",
            self.apiGroup
        )
        self.baseUrlEdit = LineEdit(self.baseUrlCard)
        self.baseUrlEdit.setText(str(cfg.base_url.value))
        self.baseUrlEdit.setFixedWidth(200)
        self.baseUrlCard.hBoxLayout.addWidget(self.baseUrlEdit)
        self.baseUrlCard.hBoxLayout.addSpacing(16)

        self.modelNameCard = SettingCard(
            FIF.ROBOT,
            "模型名称",
            "调用的模型名称",
            self.apiGroup
        )
        self.modelNameEdit = LineEdit(self.modelNameCard)
        self.modelNameEdit.setText(str(cfg.model_name.value))
        self.modelNameEdit.setFixedWidth(200)
        self.modelNameCard.hBoxLayout.addWidget(self.modelNameEdit)
        self.modelNameCard.hBoxLayout.addSpacing(16)

        self.apiKeyCard = SettingCard(
            FIF.FINGERPRINT,
            "API Key",
            "访问接口的密钥",
            self.apiGroup
        )
        self.apiKeyEdit = PasswordLineEdit(self.apiKeyCard)
        self.apiKeyEdit.setText(str(cfg.api_key.value))
        self.apiKeyEdit.setFixedWidth(200)
        self.apiKeyCard.hBoxLayout.addWidget(self.apiKeyEdit)
        self.apiKeyCard.hBoxLayout.addSpacing(16)

        self.apiGroup.addSettingCard(self.baseUrlCard)
        self.apiGroup.addSettingCard(self.modelNameCard)
        self.apiGroup.addSettingCard(self.apiKeyCard)

        self.vBoxLayout.addWidget(self.apiGroup)
        self.vBoxLayout.addStretch(1)

    def saveSettings(self):
        cfg.set(cfg.base_url, self.baseUrlEdit.text())
        cfg.set(cfg.model_name, self.modelNameEdit.text())
        cfg.set(cfg.api_key, self.apiKeyEdit.text())
        cfg.save()
