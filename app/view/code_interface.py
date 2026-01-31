import os

import qfluentwidgets as qfw
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QFrame, QTreeWidgetItem

import app.view.custom_widget as custom

class CodeInterface(QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self._parent = parent
        self.setObjectName("codeInterface")
        
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        
        self.leftContainer = QFrame(self)
        self.leftContainer.setFixedWidth(200)
        self.leftLayout = QVBoxLayout(self.leftContainer)
        self.leftLayout.setContentsMargins(8, 8, 8, 8)

        self.rightContainer = QFrame(self)
        self.rightLayout = QVBoxLayout(self.rightContainer)
        self.rightLayout.setContentsMargins(8, 8, 8, 8)
        self.fileDetailStackWidget = custom.FileDetailStackWidget(self.rightContainer)
        self.rightLayout.addWidget(self.fileDetailStackWidget)
        
        self.hBoxLayout.addWidget(self.leftContainer)
        self.hBoxLayout.addWidget(self.rightContainer)
        
        self._initLeftPanel()

    def _initLeftPanel(self) -> None:
        self.openFolderBtn = qfw.PrimaryPushButton(qfw.FluentIcon.FOLDER, "打开文件夹", self.leftContainer)
        self.openFolderBtn.clicked.connect(self._onOpenFolderClicked)
        self.leftLayout.addWidget(self.openFolderBtn)
        
        self.treeWidget = qfw.TreeWidget(self.leftContainer)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.hide()
        self.treeWidget.itemClicked.connect(self._onTreeItemClicked)
        self.leftLayout.addWidget(self.treeWidget)
        
        self.customArea = custom.FileUploadArea(self.leftContainer)
        self.customArea.fileMoved.connect(self._refreshTree)
        self.leftLayout.addWidget(self.customArea, 0, Qt.AlignmentFlag.AlignBottom)
        
        self.currentRootPath = None

    def _onOpenFolderClicked(self) -> None:
        folderPath = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folderPath:
            self.currentRootPath = folderPath
            self.openFolderBtn.hide()
            self.treeWidget.show()
            self.customArea.setContext(self.treeWidget, folderPath)
            self._populateTree(folderPath)

    def _populateTree(self, path: str) -> None:
        self.treeWidget.clear()
        
        def addItems(parent_item, current_path: str):
            try:
                entries = sorted(os.listdir(current_path))
            except OSError:
                return

            for entry in entries:
                full_path = os.path.join(current_path, entry)
                item = QTreeWidgetItem([entry])
                item.setData(0, Qt.ItemDataRole.UserRole, full_path)
                
                if parent_item:
                    parent_item.addChild(item)
                else:
                    self.treeWidget.addTopLevelItem(item)
                
                if os.path.isdir(full_path):
                    addItems(item, full_path)
        
        addItems(None, path)

    def _refreshTree(self) -> None:
        if self.currentRootPath:
            self._populateTree(self.currentRootPath)

    def _onTreeItemClicked(self, item: QTreeWidgetItem, column: int) -> None:
        path = item.data(0, Qt.ItemDataRole.UserRole)
        self._showFileInfo(path)

    def _showFileInfo(self, path: str) -> None:
        self.fileDetailStackWidget.updateFile(path)
