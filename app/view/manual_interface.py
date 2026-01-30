import qfluentwidgets as qfw


class ManualInterface(qfw.ScrollArea):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self._parent = parent
        self.setObjectName("manualInterface")
        self.setStyleSheet("background-color: transparent;")
