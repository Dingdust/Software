from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from qfluentwidgets import ScrollArea, TitleLabel, BodyLabel, CardWidget

class ManualInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("manualInterface")
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setStyleSheet("background-color: transparent;")
        
        self.scrollWidget = QWidget()
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)
        self.setWidget(self.scrollWidget)
        self.scrollWidget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)
        
        self.titleLabel = TitleLabel("使用说明手册", self.scrollWidget)
        self.contentLabel = BodyLabel(
            """
            <h2>软件著作权自动材料生成工具使用说明</h2>
            <p>本工具旨在帮助开发者快速生成软件著作权申请所需的文档材料。</p>
            <h3>1. 基本信息填写</h3>
            <p>在主界面左侧填写软件名称、版本号及简要说明。</p>
            <h3>2. 代码导入</h3>
            <p>在“代码”页导入您的源代码文件，系统将自动进行清洗和格式化。</p>
            <h3>3. 生成材料</h3>
            <p>点击“生成材料”按钮，即可导出Word或PDF格式的申请文档。</p>
            """, 
            self.scrollWidget
        )
        self.contentLabel.setWordWrap(True)
        
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.addStretch(1)
