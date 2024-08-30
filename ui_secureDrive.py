# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'secureDrive.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QScrollArea,
    QSizePolicy, QStackedWidget, QVBoxLayout, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(940, 517)
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        MainWindow.setStyleSheet(u"background-color: rgb(6, 6, 6);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_12 = QGridLayout(self.centralwidget)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.sidebar = QWidget(self.centralwidget)
        self.sidebar.setObjectName(u"sidebar")
        self.sidebar.setMaximumSize(QSize(65, 500))
        self.sidebar.setStyleSheet(u"QWidget{\n"
"background-color: rgb(76, 76, 76);\n"
"}\n"
"QPushButton{\n"
"	color:white;\n"
"	height:70px;\n"
"	width:10px;\n"
"	border:none;\n"
"}\n"
"QPushButton:checked{\n"
"	background-color:#F5FAFE;\n"
"	color:#1F95EF;\n"
"	font-weight:bold;\n"
"	border:none;\n"
"}")
        self.verticalLayout_7 = QVBoxLayout(self.sidebar)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.Secure_drive_logo = QLabel(self.sidebar)
        self.Secure_drive_logo.setObjectName(u"Secure_drive_logo")
        self.Secure_drive_logo.setMinimumSize(QSize(40, 40))
        self.Secure_drive_logo.setMaximumSize(QSize(40, 40))
        self.Secure_drive_logo.setPixmap(QPixmap(u"icons/Logo - Secure Drive.png"))
        self.Secure_drive_logo.setScaledContents(True)

        self.horizontalLayout.addWidget(self.Secure_drive_logo)


        self.verticalLayout_7.addLayout(self.horizontalLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Home = QPushButton(self.sidebar)
        self.Home.setObjectName(u"Home")
        icon = QIcon()
        icon.addFile(u":/icons/icons8-home-50.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Home.setIcon(icon)
        self.Home.setCheckable(True)
        self.Home.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.Home)

        self.Protection = QPushButton(self.sidebar)
        self.Protection.setObjectName(u"Protection")
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons8-protect-50.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Protection.setIcon(icon1)
        self.Protection.setCheckable(True)
        self.Protection.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.Protection)

        self.Notification = QPushButton(self.sidebar)
        self.Notification.setObjectName(u"Notification")
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons8-notification-50.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Notification.setIcon(icon2)
        self.Notification.setCheckable(True)
        self.Notification.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.Notification)

        self.About = QPushButton(self.sidebar)
        self.About.setObjectName(u"About")
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons8-help-50.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.About.setIcon(icon3)
        self.About.setCheckable(True)
        self.About.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.About)

        self.settings = QPushButton(self.sidebar)
        self.settings.setObjectName(u"settings")
        icon4 = QIcon()
        icon4.addFile(u":/icons/icons8-settings-50.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.settings.setIcon(icon4)
        self.settings.setCheckable(True)
        self.settings.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.settings)


        self.verticalLayout_7.addLayout(self.verticalLayout)


        self.gridLayout_12.addWidget(self.sidebar, 0, 0, 1, 1)

        self.main_menu = QWidget(self.centralwidget)
        self.main_menu.setObjectName(u"main_menu")
        self.gridLayout_3 = QGridLayout(self.main_menu)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.stackedWidget = QStackedWidget(self.main_menu)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.Homepage = QWidget()
        self.Homepage.setObjectName(u"Homepage")
        self.Catc_line_widget = QWidget(self.Homepage)
        self.Catc_line_widget.setObjectName(u"Catc_line_widget")
        self.Catc_line_widget.setGeometry(QRect(0, 0, 861, 58))
        self.horizontalLayout_2 = QHBoxLayout(self.Catc_line_widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.catch_line = QLabel(self.Catc_line_widget)
        self.catch_line.setObjectName(u"catch_line")
        font = QFont()
        font.setFamilies([u"Sitka"])
        font.setPointSize(15)
        font.setBold(False)
        font.setItalic(False)
        self.catch_line.setFont(font)
        self.catch_line.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 15pt \"Sitka\";")

        self.horizontalLayout_2.addWidget(self.catch_line)

        self.System_scan_widget = QWidget(self.Homepage)
        self.System_scan_widget.setObjectName(u"System_scan_widget")
        self.System_scan_widget.setGeometry(QRect(20, 90, 270, 141))
        self.System_scan_widget.setStyleSheet(u"QWidget{\n"
"background-color: rgb(76, 76, 76);\n"
"border-radius: 12px;\n"
"}")
        self.gridLayout_5 = QGridLayout(self.System_scan_widget)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.System_scan_title = QLabel(self.System_scan_widget)
        self.System_scan_title.setObjectName(u"System_scan_title")
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        self.System_scan_title.setFont(font1)
        self.System_scan_title.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.System_scan_title.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.System_scan_title, 0, 1, 1, 2)

        self.System_scan_logo = QPushButton(self.System_scan_widget)
        self.System_scan_logo.setObjectName(u"System_scan_logo")
        self.System_scan_logo.setMaximumSize(QSize(90, 90))
        self.System_scan_logo.setStyleSheet(u"border:none;")
        icon5 = QIcon()
        icon5.addFile(u"icons/system scan.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.System_scan_logo.setIcon(icon5)
        self.System_scan_logo.setIconSize(QSize(80, 100))

        self.gridLayout_5.addWidget(self.System_scan_logo, 1, 0, 3, 2)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_6 = QLabel(self.System_scan_widget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(160, 16777215))
        font2 = QFont()
        font2.setPointSize(8)
        font2.setBold(True)
        self.label_6.setFont(font2)
        self.label_6.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.verticalLayout_6.addWidget(self.label_6)

        self.label_7 = QLabel(self.System_scan_widget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(140, 16777215))
        self.label_7.setFont(font2)
        self.label_7.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.verticalLayout_6.addWidget(self.label_7)

        self.label_8 = QLabel(self.System_scan_widget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(140, 16777215))
        self.label_8.setFont(font2)
        self.label_8.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.verticalLayout_6.addWidget(self.label_8)


        self.gridLayout_5.addLayout(self.verticalLayout_6, 2, 2, 1, 2)

        self.File_Scan_widget = QWidget(self.Homepage)
        self.File_Scan_widget.setObjectName(u"File_Scan_widget")
        self.File_Scan_widget.setGeometry(QRect(300, 90, 244, 141))
        self.File_Scan_widget.setStyleSheet(u"QWidget{\n"
"background-color: rgb(76, 76, 76);\n"
"border-radius: 12px;\n"
"}")
        self.gridLayout_9 = QGridLayout(self.File_Scan_widget)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.File_scan_title = QLabel(self.File_Scan_widget)
        self.File_scan_title.setObjectName(u"File_scan_title")
        self.File_scan_title.setFont(font1)
        self.File_scan_title.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.File_scan_title.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.File_scan_title, 0, 1, 2, 3)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.File_scan_logo = QPushButton(self.File_Scan_widget)
        self.File_scan_logo.setObjectName(u"File_scan_logo")
        self.File_scan_logo.setMaximumSize(QSize(80, 80))
        self.File_scan_logo.setStyleSheet(u"border:none;")
        icon6 = QIcon()
        icon6.addFile(u":/icons/File scan.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.File_scan_logo.setIcon(icon6)
        self.File_scan_logo.setIconSize(QSize(100, 100))

        self.verticalLayout_9.addWidget(self.File_scan_logo)


        self.gridLayout_9.addLayout(self.verticalLayout_9, 2, 0, 3, 2)

        self.File_scan_info = QVBoxLayout()
        self.File_scan_info.setObjectName(u"File_scan_info")
        self.label_9 = QLabel(self.File_Scan_widget)
        self.label_9.setObjectName(u"label_9")
        font3 = QFont()
        font3.setBold(True)
        self.label_9.setFont(font3)
        self.label_9.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.File_scan_info.addWidget(self.label_9)

        self.label_10 = QLabel(self.File_Scan_widget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFont(font3)
        self.label_10.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.File_scan_info.addWidget(self.label_10)

        self.label_11 = QLabel(self.File_Scan_widget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFont(font3)
        self.label_11.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.File_scan_info.addWidget(self.label_11)


        self.gridLayout_9.addLayout(self.File_scan_info, 3, 2, 2, 3)

        self.Real_time_scan_widget = QWidget(self.Homepage)
        self.Real_time_scan_widget.setObjectName(u"Real_time_scan_widget")
        self.Real_time_scan_widget.setGeometry(QRect(570, 90, 251, 141))
        self.Real_time_scan_widget.setStyleSheet(u"QWidget{\n"
"background-color: rgb(76, 76, 76);\n"
"border-radius: 12px;\n"
"}")
        self.gridLayout_8 = QGridLayout(self.Real_time_scan_widget)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.Real_time_scan_info = QVBoxLayout()
        self.Real_time_scan_info.setObjectName(u"Real_time_scan_info")
        self.label_17 = QLabel(self.Real_time_scan_widget)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setFont(font3)
        self.label_17.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.Real_time_scan_info.addWidget(self.label_17)

        self.label_18 = QLabel(self.Real_time_scan_widget)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setFont(font3)
        self.label_18.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.Real_time_scan_info.addWidget(self.label_18)

        self.label_19 = QLabel(self.Real_time_scan_widget)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFont(font3)
        self.label_19.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.Real_time_scan_info.addWidget(self.label_19)


        self.gridLayout_8.addLayout(self.Real_time_scan_info, 3, 2, 1, 3)

        self.Real_time_scan_logo = QPushButton(self.Real_time_scan_widget)
        self.Real_time_scan_logo.setObjectName(u"Real_time_scan_logo")
        self.Real_time_scan_logo.setMaximumSize(QSize(80, 80))
        self.Real_time_scan_logo.setStyleSheet(u"border:none;")
        icon7 = QIcon()
        icon7.addFile(u":/icons/Real time scan.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Real_time_scan_logo.setIcon(icon7)
        self.Real_time_scan_logo.setIconSize(QSize(80, 100))

        self.gridLayout_8.addWidget(self.Real_time_scan_logo, 2, 0, 2, 2)

        self.Real_time_scan_title = QLabel(self.Real_time_scan_widget)
        self.Real_time_scan_title.setObjectName(u"Real_time_scan_title")
        self.Real_time_scan_title.setFont(font1)
        self.Real_time_scan_title.setStyleSheet(u"color: rgb(255, 255, 255);")
        self.Real_time_scan_title.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.Real_time_scan_title, 0, 1, 2, 3)

        self.Email_Breacher_check_Widget = QWidget(self.Homepage)
        self.Email_Breacher_check_Widget.setObjectName(u"Email_Breacher_check_Widget")
        self.Email_Breacher_check_Widget.setGeometry(QRect(100, 280, 241, 151))
        self.Email_Breacher_check_Widget.setStyleSheet(u"QWidget{\n"
"background-color: rgb(76, 76, 76);\n"
"border-radius: 12px;\n"
"}")
        self.gridLayout_7 = QGridLayout(self.Email_Breacher_check_Widget)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.Email_breacher_title = QHBoxLayout()
        self.Email_breacher_title.setObjectName(u"Email_breacher_title")
        self.label_15 = QLabel(self.Email_Breacher_check_Widget)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font1)
        self.label_15.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.Email_breacher_title.addWidget(self.label_15)


        self.gridLayout_7.addLayout(self.Email_breacher_title, 0, 0, 1, 2)

        self.pushButton_9 = QPushButton(self.Email_Breacher_check_Widget)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setMaximumSize(QSize(100, 110))
        self.pushButton_9.setStyleSheet(u"border:none;")
        icon8 = QIcon()
        icon8.addFile(u":/icons/check-mail.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_9.setIcon(icon8)
        self.pushButton_9.setIconSize(QSize(90, 90))

        self.gridLayout_7.addWidget(self.pushButton_9, 1, 0, 3, 1)

        self.Email_breacher_info = QVBoxLayout()
        self.Email_breacher_info.setObjectName(u"Email_breacher_info")
        self.label_20 = QLabel(self.Email_Breacher_check_Widget)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFont(font3)
        self.label_20.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.Email_breacher_info.addWidget(self.label_20)

        self.label_21 = QLabel(self.Email_Breacher_check_Widget)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setFont(font3)
        self.label_21.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.Email_breacher_info.addWidget(self.label_21)

        self.label_22 = QLabel(self.Email_Breacher_check_Widget)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFont(font3)
        self.label_22.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.Email_breacher_info.addWidget(self.label_22)


        self.gridLayout_7.addLayout(self.Email_breacher_info, 2, 1, 1, 1)

        self.Password_breacher_widget = QWidget(self.Homepage)
        self.Password_breacher_widget.setObjectName(u"Password_breacher_widget")
        self.Password_breacher_widget.setGeometry(QRect(390, 280, 261, 151))
        self.Password_breacher_widget.setStyleSheet(u"QWidget{\n"
"background-color: rgb(76, 76, 76);\n"
"border-radius: 12px;\n"
"}")
        self.gridLayout_6 = QGridLayout(self.Password_breacher_widget)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.Password_breach_title = QHBoxLayout()
        self.Password_breach_title.setObjectName(u"Password_breach_title")
        self.Password_breach_title_2 = QLabel(self.Password_breacher_widget)
        self.Password_breach_title_2.setObjectName(u"Password_breach_title_2")
        self.Password_breach_title_2.setFont(font1)
        self.Password_breach_title_2.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.Password_breach_title.addWidget(self.Password_breach_title_2)


        self.gridLayout_6.addLayout(self.Password_breach_title, 0, 0, 1, 2)

        self.Password_breach_logo = QPushButton(self.Password_breacher_widget)
        self.Password_breach_logo.setObjectName(u"Password_breach_logo")
        self.Password_breach_logo.setMaximumSize(QSize(100, 100))
        self.Password_breach_logo.setStyleSheet(u"border:none;")
        icon9 = QIcon()
        icon9.addFile(u":/icons/Password check.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.Password_breach_logo.setIcon(icon9)
        self.Password_breach_logo.setIconSize(QSize(80, 100))

        self.gridLayout_6.addWidget(self.Password_breach_logo, 1, 0, 3, 1)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_23 = QLabel(self.Password_breacher_widget)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setFont(font3)
        self.label_23.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.verticalLayout_5.addWidget(self.label_23)

        self.label_24 = QLabel(self.Password_breacher_widget)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFont(font3)
        self.label_24.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.verticalLayout_5.addWidget(self.label_24)

        self.label_25 = QLabel(self.Password_breacher_widget)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFont(font3)
        self.label_25.setStyleSheet(u"color: rgb(255, 255, 255);")

        self.verticalLayout_5.addWidget(self.label_25)


        self.gridLayout_6.addLayout(self.verticalLayout_5, 2, 1, 1, 1)

        self.stackedWidget.addWidget(self.Homepage)
        self.Protection_page = QWidget()
        self.Protection_page.setObjectName(u"Protection_page")
        self.Protection_page_catch_line = QWidget(self.Protection_page)
        self.Protection_page_catch_line.setObjectName(u"Protection_page_catch_line")
        self.Protection_page_catch_line.setGeometry(QRect(0, 0, 811, 71))
        self.verticalLayout_4 = QVBoxLayout(self.Protection_page_catch_line)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.Protection_catch_line = QLabel(self.Protection_page_catch_line)
        self.Protection_catch_line.setObjectName(u"Protection_catch_line")
        font4 = QFont()
        font4.setFamilies([u"MS Shell Dlg 2"])
        font4.setPointSize(18)
        font4.setBold(False)
        font4.setItalic(False)
        self.Protection_catch_line.setFont(font4)
        self.Protection_catch_line.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 75 18pt \"MS Shell Dlg 2\";")

        self.verticalLayout_4.addWidget(self.Protection_catch_line)

        self.Protection_page_imag_widgete = QWidget(self.Protection_page)
        self.Protection_page_imag_widgete.setObjectName(u"Protection_page_imag_widgete")
        self.Protection_page_imag_widgete.setGeometry(QRect(0, 80, 821, 384))
        self.gridLayout_10 = QGridLayout(self.Protection_page_imag_widgete)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.Protection_image = QLabel(self.Protection_page_imag_widgete)
        self.Protection_image.setObjectName(u"Protection_image")
        self.Protection_image.setPixmap(QPixmap(u":/icons/Real time.png"))
        self.Protection_image.setScaledContents(False)
        self.Protection_image.setAlignment(Qt.AlignCenter)

        self.gridLayout_10.addWidget(self.Protection_image, 0, 0, 1, 1)

        self.protection_switch = QPushButton(self.Protection_page_imag_widgete)
        self.protection_switch.setObjectName(u"protection_switch")
        icon10 = QIcon()
        icon10.addFile(u":/icons/off-button.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon10.addFile(u":/icons/toggle-button.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        icon10.addFile(u":/icons/off-button.png", QSize(), QIcon.Mode.Disabled, QIcon.State.Off)
        icon10.addFile(u":/icons/off-button.png", QSize(), QIcon.Mode.Active, QIcon.State.Off)
        self.protection_switch.setIcon(icon10)
        self.protection_switch.setIconSize(QSize(70, 70))
        self.protection_switch.setCheckable(True)

        self.gridLayout_10.addWidget(self.protection_switch, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.Protection_page)
        self.Notification_page = QWidget()
        self.Notification_page.setObjectName(u"Notification_page")
        self.Notification_title = QWidget(self.Notification_page)
        self.Notification_title.setObjectName(u"Notification_title")
        self.Notification_title.setGeometry(QRect(0, 10, 821, 52))
        self.gridLayout_11 = QGridLayout(self.Notification_title)
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.Notification_2 = QLabel(self.Notification_title)
        self.Notification_2.setObjectName(u"Notification_2")
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(15)
        font5.setBold(False)
        font5.setItalic(False)
        self.Notification_2.setFont(font5)
        self.Notification_2.setStyleSheet(u"font: 75 15pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);")

        self.gridLayout_11.addWidget(self.Notification_2, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.Notification_page)
        self.About_page = QWidget()
        self.About_page.setObjectName(u"About_page")
        self.Help_widget = QWidget(self.About_page)
        self.Help_widget.setObjectName(u"Help_widget")
        self.Help_widget.setGeometry(QRect(0, 0, 831, 61))
        self.gridLayout = QGridLayout(self.Help_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.Help_Guide = QLabel(self.Help_widget)
        self.Help_Guide.setObjectName(u"Help_Guide")
        font6 = QFont()
        font6.setFamilies([u"MS Shell Dlg 2"])
        font6.setPointSize(10)
        font6.setBold(False)
        font6.setItalic(False)
        self.Help_Guide.setFont(font6)
        self.Help_Guide.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 10pt \"MS Shell Dlg 2\";")

        self.gridLayout.addWidget(self.Help_Guide, 0, 0, 1, 1)

        self.Scroll_widget = QWidget(self.About_page)
        self.Scroll_widget.setObjectName(u"Scroll_widget")
        self.Scroll_widget.setGeometry(QRect(0, 80, 831, 391))
        self.gridLayout_2 = QGridLayout(self.Scroll_widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.Pdf_scroller = QScrollArea(self.Scroll_widget)
        self.Pdf_scroller.setObjectName(u"Pdf_scroller")
        self.Pdf_scroller.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 807, 367))
        self.Pdf_scroller.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout_2.addWidget(self.Pdf_scroller, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.About_page)
        self.settings_page = QWidget()
        self.settings_page.setObjectName(u"settings_page")
        self.Setting_title = QLabel(self.settings_page)
        self.Setting_title.setObjectName(u"Setting_title")
        self.Setting_title.setGeometry(QRect(-2, -9, 821, 51))
        self.Setting_title.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"font: 15pt \"Sitka\";")
        self.Setting_options = QWidget(self.settings_page)
        self.Setting_options.setObjectName(u"Setting_options")
        self.Setting_options.setGeometry(QRect(50, 100, 682, 202))
        self.Setting_options.setStyleSheet(u"QWidget{\n"
"background-color: rgb(76, 76, 76);\n"
"\n"
"}")
        self.gridLayout_13 = QGridLayout(self.Setting_options)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.pushButton_6 = QPushButton(self.Setting_options)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setStyleSheet(u"QPushButton{\n"
"border:none;\n"
"	color: rgb(255, 255, 255);\n"
"	font: 12pt \"MS Shell Dlg 2\";\n"
"	text-align: left;\n"
"}")

        self.gridLayout_13.addWidget(self.pushButton_6, 0, 0, 1, 2)

        self.label_2 = QLabel(self.Setting_options)
        self.label_2.setObjectName(u"label_2")
        font7 = QFont()
        font7.setFamilies([u"MS Shell Dlg 2"])
        font7.setPointSize(6)
        font7.setBold(False)
        font7.setItalic(False)
        self.label_2.setFont(font7)
        self.label_2.setStyleSheet(u"QLabel{\n"
"font: 6pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);\n"
"}")

        self.gridLayout_13.addWidget(self.label_2, 1, 0, 1, 1)

        self.line_2 = QFrame(self.Setting_options)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_13.addWidget(self.line_2, 2, 0, 1, 3)

        self.pushButton = QPushButton(self.Setting_options)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"QPushButton{\n"
"border:none;\n"
"	color: rgb(255, 255, 255);\n"
"	font: 12pt \"MS Shell Dlg 2\";\n"
"	text-align: left;\n"
"}")

        self.gridLayout_13.addWidget(self.pushButton, 3, 0, 2, 1)

        self.pushButton_2 = QPushButton(self.Setting_options)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u"QPushButton{\n"
"border:none;\n"
"text-align:right;\n"
"}")
        icon11 = QIcon()
        icon11.addFile(u":/icons/off-button.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        icon11.addFile(u":/icons/toggle-button.png", QSize(), QIcon.Mode.Normal, QIcon.State.On)
        self.pushButton_2.setIcon(icon11)
        self.pushButton_2.setIconSize(QSize(60, 60))

        self.gridLayout_13.addWidget(self.pushButton_2, 3, 2, 3, 1)

        self.label_3 = QLabel(self.Setting_options)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"QLabel{\n"
"font: 6pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);\n"
"}")

        self.gridLayout_13.addWidget(self.label_3, 5, 0, 1, 1)

        self.line_6 = QFrame(self.Setting_options)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_13.addWidget(self.line_6, 6, 0, 1, 3)

        self.pushButton_3 = QPushButton(self.Setting_options)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u"QPushButton{\n"
"border:none;\n"
"	color: rgb(255, 255, 255);\n"
"	font: 12pt \"MS Shell Dlg 2\";\n"
"	text-align: left;\n"
"}")

        self.gridLayout_13.addWidget(self.pushButton_3, 7, 0, 1, 2)

        self.label_4 = QLabel(self.Setting_options)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"QLabel{\n"
"font: 6pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);\n"
"}")

        self.gridLayout_13.addWidget(self.label_4, 8, 0, 1, 1)

        self.stackedWidget.addWidget(self.settings_page)
        self.Languages = QWidget()
        self.Languages.setObjectName(u"Languages")
        self.widget = QWidget(self.Languages)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(-10, 0, 831, 50))
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        font8 = QFont()
        font8.setFamilies([u"MS Shell Dlg 2"])
        font8.setPointSize(14)
        font8.setBold(False)
        font8.setItalic(False)
        self.label.setFont(font8)
        self.label.setStyleSheet(u"QLabel{\n"
"	font: 75 14pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 255, 255);\n"
"}\n"
"")

        self.verticalLayout_3.addWidget(self.label)

        self.Languages_opt = QWidget(self.Languages)
        self.Languages_opt.setObjectName(u"Languages_opt")
        self.Languages_opt.setGeometry(QRect(40, 119, 701, 212))
        self.Languages_opt.setStyleSheet(u"QWidget{\n"
"\n"
"background-color: rgb(76, 76, 76);\n"
"}")
        self.gridLayout_4 = QGridLayout(self.Languages_opt)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.English = QPushButton(self.Languages_opt)
        self.English.setObjectName(u"English")
        self.English.setStyleSheet(u"QPushButton{\n"
"border:none;\n"
"	color: rgb(255, 255, 255);\n"
"	font: 12pt \"MS Shell Dlg 2\";\n"
"	text-align: left;\n"
"}")

        self.verticalLayout_2.addWidget(self.English)

        self.line = QFrame(self.Languages_opt)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.Hindi = QPushButton(self.Languages_opt)
        self.Hindi.setObjectName(u"Hindi")
        self.Hindi.setStyleSheet(u"QPushButton{\n"
"border:none;\n"
"	color: rgb(255, 255, 255);\n"
"	font: 12pt \"MS Shell Dlg 2\";\n"
"text-align: left;\n"
"}")

        self.verticalLayout_2.addWidget(self.Hindi)

        self.line_3 = QFrame(self.Languages_opt)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_3)

        self.Marathi = QPushButton(self.Languages_opt)
        self.Marathi.setObjectName(u"Marathi")
        self.Marathi.setStyleSheet(u"QPushButton{\n"
"border:none;\n"
"	color: rgb(255, 255, 255);\n"
"	font: 12pt \"MS Shell Dlg 2\";\n"
"text-align: left;\n"
"}")

        self.verticalLayout_2.addWidget(self.Marathi)

        self.line_4 = QFrame(self.Languages_opt)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_4)

        self.Chinese = QPushButton(self.Languages_opt)
        self.Chinese.setObjectName(u"Chinese")
        self.Chinese.setStyleSheet(u"QPushButton{\n"
"border:none;\n"
"	color: rgb(255, 255, 255);\n"
"	font: 12pt \"MS Shell Dlg 2\";\n"
"	text-align:left;\n"
"}")

        self.verticalLayout_2.addWidget(self.Chinese)

        self.line_5 = QFrame(self.Languages_opt)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_5)

        self.Japanese = QPushButton(self.Languages_opt)
        self.Japanese.setObjectName(u"Japanese")
        self.Japanese.setStyleSheet(u"QPushButton{\n"
"border:none;\n"
"	color: rgb(255, 255, 255);\n"
"	font: 12pt \"MS Shell Dlg 2\";\n"
"	text-align: left;\n"
"}")

        self.verticalLayout_2.addWidget(self.Japanese)


        self.gridLayout_4.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.Languages)

        self.gridLayout_3.addWidget(self.stackedWidget, 1, 0, 1, 1)


        self.gridLayout_12.addWidget(self.main_menu, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.protection_switch.pressed.connect(self.protection_switch.animateClick)
        self.Notification.clicked.connect(self.stackedWidget.show)
        self.settings.clicked.connect(self.stackedWidget.show)
        self.pushButton_2.clicked["bool"].connect(self.pushButton_2.animateClick)
        self.pushButton_6.clicked.connect(self.pushButton_6.show)
        self.pushButton.clicked.connect(self.Notification.toggle)
        self.Protection.toggled.connect(self.stackedWidget.show)
        self.Home.clicked.connect(self.stackedWidget.show)
        self.About.clicked.connect(self.Scroll_widget.show)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.Secure_drive_logo.setText("")
        self.Home.setText("")
        self.Protection.setText("")
        self.Notification.setText("")
        self.About.setText("")
        self.settings.setText("")
        self.catch_line.setText(QCoreApplication.translate("MainWindow", u"Stay Secure, Stay Confident with Secure Drive", None))
        self.System_scan_title.setText(QCoreApplication.translate("MainWindow", u"System Scan", None))
        self.System_scan_logo.setText("")
#if QT_CONFIG(shortcut)
        self.System_scan_logo.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"System Scan Detects", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"And Quarantines ", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Harmful Files", None))
        self.File_scan_title.setText(QCoreApplication.translate("MainWindow", u"File Scan", None))
        self.File_scan_logo.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"File scan checks ", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Selected files for", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Threats and reports", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Files are scanned", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Automatically for ", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Creation for threats", None))
        self.Real_time_scan_logo.setText("")
        self.Real_time_scan_title.setText(QCoreApplication.translate("MainWindow", u"Real-Time Scan", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Email-Breach Checker", None))
        self.pushButton_9.setText("")
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Check emails for", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Breaches and  ", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"get advice", None))
        self.Password_breach_title_2.setText(QCoreApplication.translate("MainWindow", u"Password Breach Checker", None))
        self.Password_breach_logo.setText("")
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Check password", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"exposure and", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"get advice.", None))
        self.Protection_catch_line.setText(QCoreApplication.translate("MainWindow", u"Seamless Security with the Real-time Detection", None))
        self.Protection_image.setText("")
        self.protection_switch.setText("")
        self.Notification_2.setText(QCoreApplication.translate("MainWindow", u"Notifications", None))
        self.Help_Guide.setText(QCoreApplication.translate("MainWindow", u"Help and Guides", None))
        self.Setting_title.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Choose a language", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Change the product langauge", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Notification", None))
        self.pushButton_2.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Get product relation information", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Application Update", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Check for update", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Choose a preferred Language", None))
        self.English.setText(QCoreApplication.translate("MainWindow", u"English", None))
        self.Hindi.setText(QCoreApplication.translate("MainWindow", u"Hindi", None))
        self.Marathi.setText(QCoreApplication.translate("MainWindow", u"Marathi", None))
        self.Chinese.setText(QCoreApplication.translate("MainWindow", u"Chinese", None))
        self.Japanese.setText(QCoreApplication.translate("MainWindow", u"Japanese", None))
    # retranslateUi

