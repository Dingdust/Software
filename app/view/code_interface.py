import os
import shutil

import qfluentwidgets as qfw
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QPixmap, QMouseEvent
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QFrame, QLabel, QTreeWidgetItem


class CustomArea(QFrame):

    fileMoved = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("background-color: transparent;")
        self.setFixedHeight(64)
        
        self.vBoxLayout = QVBoxLayout(self)
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap(r"./resources/copyright.png"))
        self.label.setScaledContents(True)
        self.vBoxLayout.addWidget(self.label)
        
        self.treeWidget = None
        self.rootPath = None
        self.enabled = False

    def setContext(self, treeWidget: qfw.TreeWidget, rootPath: str) -> None:
        self.treeWidget = treeWidget
        self.rootPath = rootPath
        self.enabled = True

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if self.enabled and event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        if not self.enabled or not self.rootPath:
            return

        targetPath = self._getCurrentTargetDir()
        
        files_moved = False
        for url in event.mimeData().urls():
            srcPath = url.toLocalFile()
            if os.path.exists(srcPath):
                try:
                    dstPath = os.path.join(targetPath, os.path.basename(srcPath))
                    if srcPath != dstPath:
                        shutil.copy(srcPath, dstPath)
                        files_moved = True
                except Exception as e:
                    print(f"Error moving file {srcPath}: {e}")
        
        if files_moved:
            self.fileMoved.emit()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if not self.enabled or not self.rootPath:
            return
            
        filePath, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if filePath:
            targetPath = self._getCurrentTargetDir()
            try:
                dstPath = os.path.join(targetPath, os.path.basename(filePath))
                if filePath != dstPath:
                    shutil.move(filePath, dstPath)
                    self.fileMoved.emit()
            except Exception as e:
                print(f"Error moving file {filePath}: {e}")
        
        super().mousePressEvent(event)

    def _getCurrentTargetDir(self) -> str:
        if not self.treeWidget:
            return self.rootPath
            
        item = self.treeWidget.currentItem()
        if item:
            path = item.data(0, Qt.ItemDataRole.UserRole)
            if os.path.isdir(path):
                return path
            else:
                return os.path.dirname(path)
        return self.rootPath


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
        self.rightLayout.setContentsMargins(20, 20, 20, 20)
        self.fileInfoLabel = QLabel("Select a file to view details", self.rightContainer)
        self.fileInfoLabel.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.rightLayout.addWidget(self.fileInfoLabel)
        
        self.hBoxLayout.addWidget(self.leftContainer)
        self.hBoxLayout.addWidget(self.rightContainer)
        
        self._initLeftPanel()

    def _initLeftPanel(self) -> None:
        self.openFolderBtn = qfw.PrimaryPushButton("打开文件夹", self.leftContainer)
        self.openFolderBtn.clicked.connect(self._onOpenFolderClicked)
        self.leftLayout.addWidget(self.openFolderBtn)
        
        self.treeWidget = qfw.TreeWidget(self.leftContainer)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.hide()
        self.treeWidget.itemClicked.connect(self._onTreeItemClicked)
        self.leftLayout.addWidget(self.treeWidget)
        
        self.customArea = CustomArea(self.leftContainer)
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
        if not os.path.exists(path):
            self.fileInfoLabel.setText("File not found.")
            return
            
        info = f"Path: {path}\n"
        info += f"Size: {os.path.getsize(path)} bytes\n"
        if os.path.isdir(path):
            info += "Type: Directory"
        else:
            info += "Type: File"
            
        self.fileInfoLabel.setText(info)
