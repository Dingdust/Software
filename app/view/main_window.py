from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QIcon, QDesktopServices

from qfluentwidgets import FluentWindow
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import NavigationItemPosition

from .home_interface import HomeInterface
from .manual_interface import ManualInterface
from .code_interface import CodeInterface
from .setting_interface import SettingInterface


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        self.homeInterface = HomeInterface(self)
        self.manualInterface = ManualInterface(self)
        self.codeInterface = CodeInterface(self)
        self.settingInterface = SettingInterface(self)

        self.initNavigation()

    def initWindow(self):
        self.resize(1080, 720)
        self.setWindowIcon(QIcon("./resources/logo.jpg"))
        self.setWindowTitle("易智著——软件著作权材料生成工具")
        self.navigationInterface.setExpandWidth(150)

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, "主页")
        self.addSubInterface(self.manualInterface, FIF.BOOK_SHELF, "说明手册")
        self.addSubInterface(self.codeInterface, FIF.CODE, "软件代码")
        
        self.navigationInterface.addItem(
            routeKey="copyright",
            icon=FIF.PEOPLE,
            text="版权中心",
            onClick=self.openCopyrightWebsite,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
            tooltip="版权中心"
        )
        
        self.addSubInterface(self.settingInterface, FIF.SETTING, "设置", position=NavigationItemPosition.BOTTOM)

    @staticmethod
    def openCopyrightWebsite():
        QDesktopServices.openUrl(QUrl("https://register.ccopyright.com.cn/login.html"))
