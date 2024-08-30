# securedrive.py
from PySide6.QtWidgets import QMainWindow
from ui_secureDrive import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Secure Drive")

        self.Home.clicked.connect(self.switch_to_Homepage)
        self.Protection.clicked.connect(self.switch_to_Protection_page)
        self.Notification.clicked.connect(self.switch_to_Notification_page)
        self.About.clicked.connect(self.switch_to_About_page)
        self.settings.clicked.connect(self.switch_to_Settings_page)

    def switch_to_Homepage(self):
        self.stackedWidget.setCurrentIndex(0)

    def switch_to_Protection_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def switch_to_Notification_page(self):
        self.stackedWidget.setCurrentIndex(2)

    def switch_to_About_page(self):
        self.stackedWidget.setCurrentIndex(3)

    def switch_to_Settings_page(self):
        self.stackedWidget.setCurrentIndex(4)
