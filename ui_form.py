# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPlainTextEdit, QPushButton,
    QSizePolicy, QSlider, QStackedWidget, QStatusBar,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

from PySide6.QtWebEngineWidgets import QWebEngineView


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 1080)
        self.widget = QWidget(MainWindow)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"color: rgb(26, 95, 180);\n"
"background-color: rgb(0, 0, 0);")
        self.stackedWidget = QStackedWidget(self.widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(0, 80, 2331, 971))
        self.stackedWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.Main_pg = QWidget()
        self.Main_pg.setObjectName(u"Main_pg")
        self.Main_pg.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"")
        self.videoLabel = QLabel(self.Main_pg)
        self.videoLabel.setObjectName(u"videoLabel")
        self.videoLabel.setGeometry(QRect(1710, 720, 151, 151))
        self.verticalLayoutWidget = QWidget(self.Main_pg)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(100, 50, 1121, 591))
        self.videoLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.videoLayout.setObjectName(u"videoLayout")
        self.videoLayout.setContentsMargins(0, 0, 0, 0)
        self.screenToggler = QPushButton(self.Main_pg)
        self.screenToggler.setObjectName(u"screenToggler")
        self.screenToggler.setGeometry(QRect(100, 30, 191, 20))
        self.slamMapView = QLabel(self.Main_pg)
        self.slamMapView.setObjectName(u"slamMapView")
        self.slamMapView.setGeometry(QRect(1570, 810, 51, 20))
        self.mapToggler = QPushButton(self.Main_pg)
        self.mapToggler.setObjectName(u"mapToggler")
        self.mapToggler.setGeometry(QRect(1240, 560, 91, 21))
        self.mapToggler.setStyleSheet(u"")
        self.maincameraToggler = QPushButton(self.Main_pg)
        self.maincameraToggler.setObjectName(u"maincameraToggler")
        self.maincameraToggler.setGeometry(QRect(1700, 560, 201, 26))
        self.Velocimeter = QWidget(self.Main_pg)
        self.Velocimeter.setObjectName(u"Velocimeter")
        self.Velocimeter.setGeometry(QRect(390, 660, 391, 221))
        self.Velocimeter.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.linearspeedLabel = QLabel(self.Velocimeter)
        self.linearspeedLabel.setObjectName(u"linearspeedLabel")
        self.linearspeedLabel.setGeometry(QRect(10, 10, 311, 18))
        self.gpsLabel = QLabel(self.Velocimeter)
        self.gpsLabel.setObjectName(u"gpsLabel")
        self.gpsLabel.setGeometry(QRect(10, 40, 321, 18))
        self.distanceLabel = QLabel(self.Velocimeter)
        self.distanceLabel.setObjectName(u"distanceLabel")
        self.distanceLabel.setGeometry(QRect(10, 70, 321, 18))
        self.mapImageView = QLabel(self.Main_pg)
        self.mapImageView.setObjectName(u"mapImageView")
        self.mapImageView.setGeometry(QRect(1230, 600, 331, 331))
        self.compassLayout = QWidget(self.Main_pg)
        self.compassLayout.setObjectName(u"compassLayout")
        self.compassLayout.setGeometry(QRect(100, 660, 281, 221))
        self.secondaryCameraToggler = QPushButton(self.Main_pg)
        self.secondaryCameraToggler.setObjectName(u"secondaryCameraToggler")
        self.secondaryCameraToggler.setGeometry(QRect(1240, 20, 191, 26))
        self.verticalLayoutWidget_3 = QWidget(self.Main_pg)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(1230, 50, 681, 481))
        self.secondaryVideoLayout = QVBoxLayout(self.verticalLayoutWidget_3)
        self.secondaryVideoLayout.setObjectName(u"secondaryVideoLayout")
        self.secondaryVideoLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget.addWidget(self.Main_pg)
        self.maincameraToggler.raise_()
        self.slamMapView.raise_()
        self.videoLabel.raise_()
        self.verticalLayoutWidget.raise_()
        self.screenToggler.raise_()
        self.mapToggler.raise_()
        self.Velocimeter.raise_()
        self.mapImageView.raise_()
        self.compassLayout.raise_()
        self.secondaryCameraToggler.raise_()
        self.verticalLayoutWidget_3.raise_()
        self.Main_2_pg = QWidget()
        self.Main_2_pg.setObjectName(u"Main_2_pg")
        self.Main_2_pg.setStyleSheet(u"background-color: rgb(246, 211, 45);")
        self.screenToggler_2 = QPushButton(self.Main_2_pg)
        self.screenToggler_2.setObjectName(u"screenToggler_2")
        self.screenToggler_2.setGeometry(QRect(120, 30, 191, 20))
        self.verticalLayoutWidget_4 = QWidget(self.Main_2_pg)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(110, 50, 1121, 591))
        self.videoLayout_lq = QVBoxLayout(self.verticalLayoutWidget_4)
        self.videoLayout_lq.setObjectName(u"videoLayout_lq")
        self.videoLayout_lq.setContentsMargins(0, 0, 0, 0)
        self.verticalLayoutWidget_5 = QWidget(self.Main_2_pg)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(1240, 50, 671, 481))
        self.secondaryVideoLayout_lq = QVBoxLayout(self.verticalLayoutWidget_5)
        self.secondaryVideoLayout_lq.setObjectName(u"secondaryVideoLayout_lq")
        self.secondaryVideoLayout_lq.setContentsMargins(0, 0, 0, 0)
        self.secondaryCameraToggler_2 = QPushButton(self.Main_2_pg)
        self.secondaryCameraToggler_2.setObjectName(u"secondaryCameraToggler_2")
        self.secondaryCameraToggler_2.setGeometry(QRect(1240, 20, 191, 26))
        self.Velocimeter_2 = QWidget(self.Main_2_pg)
        self.Velocimeter_2.setObjectName(u"Velocimeter_2")
        self.Velocimeter_2.setGeometry(QRect(460, 680, 391, 221))
        self.Velocimeter_2.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.linearspeedLabel_2 = QLabel(self.Velocimeter_2)
        self.linearspeedLabel_2.setObjectName(u"linearspeedLabel_2")
        self.linearspeedLabel_2.setGeometry(QRect(10, 10, 311, 18))
        self.gpsLabel_2 = QLabel(self.Velocimeter_2)
        self.gpsLabel_2.setObjectName(u"gpsLabel_2")
        self.gpsLabel_2.setGeometry(QRect(10, 40, 321, 18))
        self.distanceLabel_2 = QLabel(self.Velocimeter_2)
        self.distanceLabel_2.setObjectName(u"distanceLabel_2")
        self.distanceLabel_2.setGeometry(QRect(10, 70, 321, 18))
        self.compassLayout_2 = QWidget(self.Main_2_pg)
        self.compassLayout_2.setObjectName(u"compassLayout_2")
        self.compassLayout_2.setGeometry(QRect(120, 680, 281, 221))
        self.stackedWidget.addWidget(self.Main_2_pg)
        self.Settings_pg = QWidget()
        self.Settings_pg.setObjectName(u"Settings_pg")
        self.stackedWidget.addWidget(self.Settings_pg)
        self.Map_pg = QWidget()
        self.Map_pg.setObjectName(u"Map_pg")
        self.Map_pg.setStyleSheet(u"background-color: rgb(87, 227, 137);")
        self.mapView = QWebEngineView(self.Map_pg)
        self.mapView.setObjectName(u"mapView")
        self.mapView.setGeometry(QRect(-1, -1, 1231, 641))
        self.verticalLayoutWidget_2 = QWidget(self.Map_pg)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(1399, 79, 351, 171))
        self.mapControlsLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.mapControlsLayout.setObjectName(u"mapControlsLayout")
        self.mapControlsLayout.setContentsMargins(0, 0, 0, 0)
        self.treeInput = QLineEdit(self.verticalLayoutWidget_2)
        self.treeInput.setObjectName(u"treeInput")

        self.mapControlsLayout.addWidget(self.treeInput)

        self.addTreeButton = QPushButton(self.verticalLayoutWidget_2)
        self.addTreeButton.setObjectName(u"addTreeButton")

        self.mapControlsLayout.addWidget(self.addTreeButton)

        self.calculatePathButton = QPushButton(self.Map_pg)
        self.calculatePathButton.setObjectName(u"calculatePathButton")
        self.calculatePathButton.setGeometry(QRect(1403, 290, 351, 26))
        self.stackedWidget.addWidget(self.Map_pg)
        self.Login_pg = QWidget()
        self.Login_pg.setObjectName(u"Login_pg")
        self.Login_pg.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.usernameField = QLineEdit(self.Login_pg)
        self.usernameField.setObjectName(u"usernameField")
        self.usernameField.setGeometry(QRect(290, 280, 241, 31))
        self.passwordField = QLineEdit(self.Login_pg)
        self.passwordField.setObjectName(u"passwordField")
        self.passwordField.setGeometry(QRect(290, 310, 241, 31))
        self.Login_Button = QPushButton(self.Login_pg)
        self.Login_Button.setObjectName(u"Login_Button")
        self.Login_Button.setGeometry(QRect(250, 380, 94, 26))
        self.loginLabel = QLabel(self.Login_pg)
        self.loginLabel.setObjectName(u"loginLabel")
        self.loginLabel.setGeometry(QRect(210, 280, 71, 21))
        self.loginLabel_2 = QLabel(self.Login_pg)
        self.loginLabel_2.setObjectName(u"loginLabel_2")
        self.loginLabel_2.setGeometry(QRect(210, 310, 71, 21))
        self.stackedWidget.addWidget(self.Login_pg)
        self.Home_pg = QWidget()
        self.Home_pg.setObjectName(u"Home_pg")
        self.Home_pg.setStyleSheet(u"background-color: rgb(220, 138, 221);")
        self.offboardButton = QPushButton(self.Home_pg)
        self.offboardButton.setObjectName(u"offboardButton")
        self.offboardButton.setGeometry(QRect(160, 120, 111, 111))
        self.armButton = QPushButton(self.Home_pg)
        self.armButton.setObjectName(u"armButton")
        self.armButton.setGeometry(QRect(160, 230, 111, 111))
        self.offboardLabel = QLabel(self.Home_pg)
        self.offboardLabel.setObjectName(u"offboardLabel")
        self.offboardLabel.setGeometry(QRect(280, 130, 171, 91))
        self.armLabel = QLabel(self.Home_pg)
        self.armLabel.setObjectName(u"armLabel")
        self.armLabel.setGeometry(QRect(280, 240, 171, 91))
        self.routerToggler = QPushButton(self.Home_pg)
        self.routerToggler.setObjectName(u"routerToggler")
        self.routerToggler.setGeometry(QRect(160, 10, 111, 111))
        self.routerLabel = QLabel(self.Home_pg)
        self.routerLabel.setObjectName(u"routerLabel")
        self.routerLabel.setGeometry(QRect(280, 20, 171, 91))
        self.localprocessButton = QPushButton(self.Home_pg)
        self.localprocessButton.setObjectName(u"localprocessButton")
        self.localprocessButton.setGeometry(QRect(160, 340, 111, 111))
        self.localprocessLabel = QLabel(self.Home_pg)
        self.localprocessLabel.setObjectName(u"localprocessLabel")
        self.localprocessLabel.setGeometry(QRect(280, 350, 171, 91))
        self.rtkToggler = QPushButton(self.Home_pg)
        self.rtkToggler.setObjectName(u"rtkToggler")
        self.rtkToggler.setGeometry(QRect(470, 10, 111, 111))
        self.gpsrtkLabel = QLabel(self.Home_pg)
        self.gpsrtkLabel.setObjectName(u"gpsrtkLabel")
        self.gpsrtkLabel.setGeometry(QRect(590, 20, 171, 91))
        self.rosoutTextEdit = QPlainTextEdit(self.Home_pg)
        self.rosoutTextEdit.setObjectName(u"rosoutTextEdit")
        self.rosoutTextEdit.setGeometry(QRect(473, 129, 371, 321))
        self.rosoutTextEdit.setReadOnly(True)
        self.safetystopButton = QPushButton(self.Home_pg)
        self.safetystopButton.setObjectName(u"safetystopButton")
        self.safetystopButton.setGeometry(QRect(160, 450, 111, 111))
        self.safetyresetButton = QPushButton(self.Home_pg)
        self.safetyresetButton.setObjectName(u"safetyresetButton")
        self.safetyresetButton.setGeometry(QRect(160, 560, 111, 111))
        self.startlidarButton = QPushButton(self.Home_pg)
        self.startlidarButton.setObjectName(u"startlidarButton")
        self.startlidarButton.setGeometry(QRect(470, 450, 111, 111))
        self.starttreedetectorButton = QPushButton(self.Home_pg)
        self.starttreedetectorButton.setObjectName(u"starttreedetectorButton")
        self.starttreedetectorButton.setGeometry(QRect(470, 560, 111, 111))
        self.stackedWidget.addWidget(self.Home_pg)
        self.Alarm_pg = QWidget()
        self.Alarm_pg.setObjectName(u"Alarm_pg")
        self.Alarm_pg.setStyleSheet(u"background-color: rgb(153, 193, 241);")
        self.AlarmPage = QWidget(self.Alarm_pg)
        self.AlarmPage.setObjectName(u"AlarmPage")
        self.AlarmPage.setGeometry(QRect(70, 0, 1231, 671))
        self.tableWidget = QTableWidget(self.AlarmPage)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(15, 1, 1301, 891))
        self.ackButton = QPushButton(self.Alarm_pg)
        self.ackButton.setObjectName(u"ackButton")
        self.ackButton.setGeometry(QRect(110, 730, 161, 26))
        self.stackedWidget.addWidget(self.Alarm_pg)
        self.sidebarWidget = QWidget(self.widget)
        self.sidebarWidget.setObjectName(u"sidebarWidget")
        self.sidebarWidget.setGeometry(QRect(0, 80, 81, 971))
        self.Home_Button = QPushButton(self.sidebarWidget)
        self.Home_Button.setObjectName(u"Home_Button")
        self.Home_Button.setGeometry(QRect(0, 0, 101, 61))
        self.Home_Button.setStyleSheet(u"QPushButton {\n"
"    background-color: none;\n"
"    color: white;\n"
"    border: none;\n"
"    text-align: left;\n"
"    padding: 8px;\n"
"}\n"
"")
        self.Main_Button = QPushButton(self.sidebarWidget)
        self.Main_Button.setObjectName(u"Main_Button")
        self.Main_Button.setGeometry(QRect(0, 60, 101, 61))
        self.Main_Button.setStyleSheet(u"QPushButton {\n"
"    background-color: none;\n"
"    color: white;\n"
"    border: none;\n"
"    text-align: left;\n"
"    padding: 8px;\n"
"}\n"
"")
        self.Alarm_Button = QPushButton(self.sidebarWidget)
        self.Alarm_Button.setObjectName(u"Alarm_Button")
        self.Alarm_Button.setGeometry(QRect(0, 120, 101, 61))
        self.Alarm_Button.setStyleSheet(u"QPushButton {\n"
"    background-color: none;\n"
"    color: white;\n"
"    border: none;\n"
"    text-align: left;\n"
"    padding: 8px;\n"
"}\n"
"")
        self.Settings_Button = QPushButton(self.sidebarWidget)
        self.Settings_Button.setObjectName(u"Settings_Button")
        self.Settings_Button.setGeometry(QRect(0, 180, 101, 61))
        self.Settings_Button.setStyleSheet(u"QPushButton {\n"
"    background-color: none;\n"
"    color: white;\n"
"    border: none;\n"
"    text-align: left;\n"
"    padding: 8px;\n"
"}\n"
"")
        self.Map_Button = QPushButton(self.sidebarWidget)
        self.Map_Button.setObjectName(u"Map_Button")
        self.Map_Button.setGeometry(QRect(0, 240, 101, 61))
        self.Map_Button.setStyleSheet(u"QPushButton {\n"
"    background-color: none;\n"
"    color: white;\n"
"    border: none;\n"
"    text-align: left;\n"
"    padding: 8px;\n"
"}\n"
"")
        self.Main_2_Button = QPushButton(self.sidebarWidget)
        self.Main_2_Button.setObjectName(u"Main_2_Button")
        self.Main_2_Button.setGeometry(QRect(0, 290, 101, 61))
        self.Main_2_Button.setStyleSheet(u"QPushButton {\n"
"    background-color: none;\n"
"    color: white;\n"
"    border: none;\n"
"    text-align: left;\n"
"    padding: 8px;\n"
"}\n"
"")
        self.statusWidget = QWidget(self.widget)
        self.statusWidget.setObjectName(u"statusWidget")
        self.statusWidget.setGeometry(QRect(-130, 0, 2461, 81))
        self.statusWidget.setStyleSheet(u"background-color: rgb(1, 1, 1);")
        self.labelTime = QLabel(self.statusWidget)
        self.labelTime.setObjectName(u"labelTime")
        self.labelTime.setGeometry(QRect(140, 10, 421, 18))
        self.labelBattery = QLabel(self.statusWidget)
        self.labelBattery.setObjectName(u"labelBattery")
        self.labelBattery.setGeometry(QRect(140, 30, 421, 18))
        self.alarmIcon = QLabel(self.statusWidget)
        self.alarmIcon.setObjectName(u"alarmIcon")
        self.alarmIcon.setGeometry(QRect(860, 20, 41, 31))
        self.alarmIcon.setPixmap(QPixmap(u"icons/greyicon.png"))
        self.alarmIcon.setScaledContents(True)
        self.labelControlMode = QLabel(self.statusWidget)
        self.labelControlMode.setObjectName(u"labelControlMode")
        self.labelControlMode.setGeometry(QRect(140, 50, 421, 18))
        self.labelTimeRemaingBattery = QLabel(self.statusWidget)
        self.labelTimeRemaingBattery.setObjectName(u"labelTimeRemaingBattery")
        self.labelTimeRemaingBattery.setGeometry(QRect(360, 30, 421, 18))
        self.labelPing = QLabel(self.statusWidget)
        self.labelPing.setObjectName(u"labelPing")
        self.labelPing.setGeometry(QRect(360, 10, 421, 18))
        self.toggleInputButton = QPushButton(self.statusWidget)
        self.toggleInputButton.setObjectName(u"toggleInputButton")
        self.toggleInputButton.setGeometry(QRect(1030, 10, 191, 21))
        self.toggleInputButton.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(245, 194, 17);")
        self.powerSlider = QSlider(self.statusWidget)
        self.powerSlider.setObjectName(u"powerSlider")
        self.powerSlider.setGeometry(QRect(1030, 40, 191, 16))
        self.powerSlider.setMaximum(100)
        self.powerSlider.setOrientation(Qt.Orientation.Horizontal)
        self.toolSlider = QSlider(self.statusWidget)
        self.toolSlider.setObjectName(u"toolSlider")
        self.toolSlider.setGeometry(QRect(1030, 60, 191, 16))
        self.toolSlider.setMaximum(100)
        self.toolSlider.setOrientation(Qt.Orientation.Horizontal)
        MainWindow.setCentralWidget(self.widget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1920, 23))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.videoLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.screenToggler.setText(QCoreApplication.translate("MainWindow", u"Turn On CSI Camera", None))
        self.slamMapView.setText("")
        self.mapToggler.setText(QCoreApplication.translate("MainWindow", u"Start Slam", None))
        self.maincameraToggler.setText(QCoreApplication.translate("MainWindow", u"Turn On RealSense Camera", None))
        self.linearspeedLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.gpsLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.distanceLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.mapImageView.setText("")
        self.secondaryCameraToggler.setText(QCoreApplication.translate("MainWindow", u"Turn On Back CSI Camera", None))
        self.screenToggler_2.setText(QCoreApplication.translate("MainWindow", u"Turn On CSI Camera", None))
        self.secondaryCameraToggler_2.setText(QCoreApplication.translate("MainWindow", u"Turn On Back CSI Camera", None))
        self.linearspeedLabel_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.gpsLabel_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.distanceLabel_2.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.addTreeButton.setText(QCoreApplication.translate("MainWindow", u"Add tree", None))
        self.calculatePathButton.setText(QCoreApplication.translate("MainWindow", u"Calculate Path", None))
        self.Login_Button.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.loginLabel.setText(QCoreApplication.translate("MainWindow", u"User:", None))
        self.loginLabel_2.setText(QCoreApplication.translate("MainWindow", u"Password:", None))
        self.offboardButton.setText(QCoreApplication.translate("MainWindow", u"OffBoard", None))
        self.armButton.setText(QCoreApplication.translate("MainWindow", u"Arming", None))
        self.offboardLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.armLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.routerToggler.setText(QCoreApplication.translate("MainWindow", u"Connect \n"
"2\n"
"Robot", None))
        self.routerLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.localprocessButton.setText(QCoreApplication.translate("MainWindow", u"Start HMI \n"
"Receiver", None))
        self.localprocessLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.rtkToggler.setText(QCoreApplication.translate("MainWindow", u"Turn\n"
"On\n"
"RTK", None))
        self.gpsrtkLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.safetystopButton.setText(QCoreApplication.translate("MainWindow", u"Trigger \n"
"Safety Stop", None))
        self.safetyresetButton.setText(QCoreApplication.translate("MainWindow", u"Trigger \n"
"Safety Reset", None))
        self.startlidarButton.setText(QCoreApplication.translate("MainWindow", u"Start \n"
"Lidar", None))
        self.starttreedetectorButton.setText(QCoreApplication.translate("MainWindow", u"Start \n"
"Tree \n"
"Detector", None))
        self.ackButton.setText(QCoreApplication.translate("MainWindow", u"Acknowledge Alarm", None))
        self.Home_Button.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.Main_Button.setText(QCoreApplication.translate("MainWindow", u"Main", None))
        self.Alarm_Button.setText(QCoreApplication.translate("MainWindow", u"Alarms", None))
        self.Settings_Button.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.Map_Button.setText(QCoreApplication.translate("MainWindow", u"Map", None))
        self.Main_2_Button.setText(QCoreApplication.translate("MainWindow", u"Main_2", None))
        self.labelTime.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.labelBattery.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.alarmIcon.setText("")
        self.labelControlMode.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.labelTimeRemaingBattery.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.labelPing.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.toggleInputButton.setText(QCoreApplication.translate("MainWindow", u"Toggle Keyboard/Controller", None))
    # retranslateUi

