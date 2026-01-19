import sys

from qfluentwidgets import setTheme
from PyQt6.QtWidgets import QApplication

from app.common.config import cfg
from app.view.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    setTheme(cfg.theme.value)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
