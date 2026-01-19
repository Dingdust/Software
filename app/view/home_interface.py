from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from qfluentwidgets import CardWidget, TitleLabel, BodyLabel, PrimaryPushButton, LineEdit, TextEdit

class HomeInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("homeInterface")
        
        # Main Layout
        self.hBoxLayout = QHBoxLayout(self)
        
        # Left Panel (Input)
        self.leftPanel = CardWidget(self)
        self.leftLayout = QVBoxLayout(self.leftPanel)
        
        self.titleLabel = TitleLabel("基本信息", self.leftPanel)
        self.nameInput = LineEdit(self.leftPanel)
        self.nameInput.setPlaceholderText("软件名称")
        self.versionInput = LineEdit(self.leftPanel)
        self.versionInput.setPlaceholderText("版本号")
        self.descInput = TextEdit(self.leftPanel)
        self.descInput.setPlaceholderText("软件说明")
        self.generateBtn = PrimaryPushButton("生成材料", self.leftPanel)
        
        self.leftLayout.addWidget(self.titleLabel)
        self.leftLayout.addWidget(self.nameInput)
        self.leftLayout.addWidget(self.versionInput)
        self.leftLayout.addWidget(self.descInput)
        self.leftLayout.addWidget(self.generateBtn)
        self.leftLayout.addStretch(1)
        
        # Right Panel (Preview/Output)
        self.rightPanel = CardWidget(self)
        self.rightLayout = QVBoxLayout(self.rightPanel)
        
        self.previewTitle = TitleLabel("生成预览", self.rightPanel)
        self.previewContent = BodyLabel("此处显示生成的材料预览...", self.rightPanel)
        
        self.rightLayout.addWidget(self.previewTitle)
        self.rightLayout.addWidget(self.previewContent)
        self.rightLayout.addStretch(1)
        
        # Add panels to main layout
        self.hBoxLayout.addWidget(self.leftPanel, 1)
        self.hBoxLayout.addWidget(self.rightPanel, 2)
