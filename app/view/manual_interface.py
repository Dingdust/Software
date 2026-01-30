import qfluentwidgets as qfw
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout


class ManualInterface(qfw.ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._parent = parent
        self.setObjectName("manualInterface")
