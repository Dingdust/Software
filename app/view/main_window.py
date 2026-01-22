import qfluentwidgets as qfw
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QIcon, QDesktopServices

from app.common.config import cfg
from .home_interface import HomeInterface
from .manual_interface import ManualInterface
from .code_interface import CodeInterface
from .setting_interface import SettingInterface


class MainWindow(qfw.FluentWindow):

    def __init__(self):
        super().__init__()
        qfw.setTheme(cfg.theme.value)

        self.initWindow()

        self.homeInterface = HomeInterface(self)
        self.manualInterface = ManualInterface(self)
        self.codeInterface = CodeInterface(self)
        self.settingInterface = SettingInterface(self)

        self.initNavigation()

    def initWindow(self):
        self.resize(960, 640)
        self.setWindowIcon(QIcon("./resources/logo.jpg"))
        self.setWindowTitle("易智著——软件著作权材料生成工具")
        self.navigationInterface.setExpandWidth(150)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, qfw.FluentIcon.HOME, "登记申请")
        self.addSubInterface(self.manualInterface, qfw.FluentIcon.BOOK_SHELF, "说明手册")
        self.addSubInterface(self.codeInterface, qfw.FluentIcon.CODE, "软件代码")

        self.navigationInterface.addItem(
            routeKey="copyright",
            icon=qfw.FluentIcon.PEOPLE,
            text="版权中心",
            onClick=self.openCopyrightWebsite,
            selectable=False,
            position=qfw.NavigationItemPosition.BOTTOM,
            tooltip="版权中心"
        )

        self.addSubInterface(self.settingInterface, qfw.FluentIcon.SETTING, "设置", position=qfw.NavigationItemPosition.BOTTOM)

    @staticmethod
    def openCopyrightWebsite():
        QDesktopServices.openUrl(QUrl("https://register.ccopyright.com.cn/login.html"))
