from PyQt6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import PlainTextEdit, TitleLabel, PrimaryPushButton

class CodeInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("codeInterface")
        
        self.vBoxLayout = QVBoxLayout(self)
        
        self.headerLayout = QVBoxLayout()
        self.titleLabel = TitleLabel("代码管理", self)
        self.importBtn = PrimaryPushButton("导入代码目录", self)
        
        self.headerLayout.addWidget(self.titleLabel)
        self.headerLayout.addWidget(self.importBtn)
        
        self.codeViewer = PlainTextEdit(self)
        self.codeViewer.setReadOnly(True)
        self.codeViewer.setPlainText("# 此处显示导入的代码...")
        
        self.vBoxLayout.addLayout(self.headerLayout)
        self.vBoxLayout.addWidget(self.codeViewer)
