# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSlider, QStackedWidget, QStatusBar, QTableWidget,
    QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget)

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
        self.stackedWidget.setGeometry(QRect(60, 80, 2271, 971))
        self.stackedWidget.setStyleSheet(u"")
        self.Main_pg = QWidget()
        self.Main_pg.setObjectName(u"Main_pg")
        self.Main_pg.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"background-color: rgb(255, 163, 72);")
        self.videoLabel = QLabel(self.Main_pg)
        self.videoLabel.setObjectName(u"videoLabel")
        self.videoLabel.setGeometry(QRect(460, 10, 441, 281))
        self.toggleInputButton = QPushButton(self.Main_pg)
        self.toggleInputButton.setObjectName(u"toggleInputButton")
        self.toggleInputButton.setGeometry(QRect(30, 500, 191, 21))
        self.toggleInputButton.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(245, 194, 17);")
        self.verticalLayoutWidget = QWidget(self.Main_pg)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 431, 281))
        self.videoLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.videoLayout.setObjectName(u"videoLayout")
        self.videoLayout.setContentsMargins(0, 0, 0, 0)
        self.powerSlider = QSlider(self.Main_pg)
        self.powerSlider.setObjectName(u"powerSlider")
        self.powerSlider.setGeometry(QRect(30, 480, 191, 16))
        self.powerSlider.setMaximum(100)
        self.powerSlider.setOrientation(Qt.Orientation.Horizontal)
        self.screenToggler = QPushButton(self.Main_pg)
        self.screenToggler.setObjectName(u"screenToggler")
        self.screenToggler.setGeometry(QRect(10, 290, 21, 21))
        self.slamMapView = QLabel(self.Main_pg)
        self.slamMapView.setObjectName(u"slamMapView")
        self.slamMapView.setGeometry(QRect(420, 370, 241, 241))
        self.mapToggler = QPushButton(self.Main_pg)
        self.mapToggler.setObjectName(u"mapToggler")
        self.mapToggler.setGeometry(QRect(280, 369, 71, 21))
        self.mapToggler.setStyleSheet(u"")
        self.stackedWidget.addWidget(self.Main_pg)
        self.Main_2_pg = QWidget()
        self.Main_2_pg.setObjectName(u"Main_2_pg")
        self.Main_2_pg.setStyleSheet(u"background-color: rgb(246, 211, 45);")
        self.widget_2 = QWidget(self.Main_2_pg)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setGeometry(QRect(-1, -1, 1221, 641))
        self.verticalLayoutWidget_2 = QWidget(self.widget_2)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(-1, -1, 1231, 641))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
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
        self.stackedWidget.addWidget(self.Map_pg)
        self.Login_pg = QWidget()
        self.Login_pg.setObjectName(u"Login_pg")
        self.Login_pg.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.usernameField = QLineEdit(self.Login_pg)
        self.usernameField.setObjectName(u"usernameField")
        self.usernameField.setGeometry(QRect(232, 275, 241, 31))
        self.passwordField = QLineEdit(self.Login_pg)
        self.passwordField.setObjectName(u"passwordField")
        self.passwordField.setGeometry(QRect(230, 320, 241, 31))
        self.textEdit = QTextEdit(self.Login_pg)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(20, 270, 201, 91))
        self.textEdit.setStyleSheet(u"border-color: rgb(255, 255, 255);")
        self.Login_Button = QPushButton(self.Login_pg)
        self.Login_Button.setObjectName(u"Login_Button")
        self.Login_Button.setGeometry(QRect(250, 380, 94, 26))
        self.stackedWidget.addWidget(self.Login_pg)
        self.Home_pg = QWidget()
        self.Home_pg.setObjectName(u"Home_pg")
        self.Home_pg.setStyleSheet(u"background-color: rgb(220, 138, 221);")
        self.offboardButton = QPushButton(self.Home_pg)
        self.offboardButton.setObjectName(u"offboardButton")
        self.offboardButton.setGeometry(QRect(40, 10, 94, 26))
        self.armButton = QPushButton(self.Home_pg)
        self.armButton.setObjectName(u"armButton")
        self.armButton.setGeometry(QRect(140, 10, 94, 26))
        self.offboardLabel = QLabel(self.Home_pg)
        self.offboardLabel.setObjectName(u"offboardLabel")
        self.offboardLabel.setGeometry(QRect(40, 40, 71, 18))
        self.armLabel = QLabel(self.Home_pg)
        self.armLabel.setObjectName(u"armLabel")
        self.armLabel.setGeometry(QRect(140, 40, 91, 18))
        self.stackedWidget.addWidget(self.Home_pg)
        self.Alarm_pg = QWidget()
        self.Alarm_pg.setObjectName(u"Alarm_pg")
        self.Alarm_pg.setStyleSheet(u"background-color: rgb(153, 193, 241);")
        self.AlarmPage = QWidget(self.Alarm_pg)
        self.AlarmPage.setObjectName(u"AlarmPage")
        self.AlarmPage.setGeometry(QRect(-1, -1, 1261, 671))
        self.tableWidget = QTableWidget(self.AlarmPage)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(15, 1, 1301, 891))
        self.ackButton = QPushButton(self.Alarm_pg)
        self.ackButton.setObjectName(u"ackButton")
        self.ackButton.setGeometry(QRect(30, 920, 161, 26))
        self.stackedWidget.addWidget(self.Alarm_pg)
        self.sidebarWidget = QWidget(self.widget)
        self.sidebarWidget.setObjectName(u"sidebarWidget")
        self.sidebarWidget.setGeometry(QRect(0, 80, 81, 961))
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
        self.statusWidget = QWidget(self.widget)
        self.statusWidget.setObjectName(u"statusWidget")
        self.statusWidget.setGeometry(QRect(-130, 0, 2461, 81))
        self.statusWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.labelTime = QLabel(self.statusWidget)
        self.labelTime.setObjectName(u"labelTime")
        self.labelTime.setGeometry(QRect(140, 10, 421, 18))
        self.labelBattery = QLabel(self.statusWidget)
        self.labelBattery.setObjectName(u"labelBattery")
        self.labelBattery.setGeometry(QRect(140, 30, 421, 18))
        self.alarmIcon = QLabel(self.statusWidget)
        self.alarmIcon.setObjectName(u"alarmIcon")
        self.alarmIcon.setGeometry(QRect(1090, 10, 41, 31))
        self.alarmIcon.setPixmap(QPixmap(u"icons/greyicon.png"))
        self.alarmIcon.setScaledContents(True)
        self.labelControlMode = QLabel(self.statusWidget)
        self.labelControlMode.setObjectName(u"labelControlMode")
        self.labelControlMode.setGeometry(QRect(140, 50, 421, 18))
        self.labelTimeRemaingBattery = QLabel(self.statusWidget)
        self.labelTimeRemaingBattery.setObjectName(u"labelTimeRemaingBattery")
        self.labelTimeRemaingBattery.setGeometry(QRect(360, 30, 421, 18))
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
        self.toggleInputButton.setText(QCoreApplication.translate("MainWindow", u"Toggle Keyboard/Controller", None))
        self.screenToggler.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.slamMapView.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.mapToggler.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.textEdit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:22pt;\">User:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:22pt;\">Password:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:22pt;\"><br /"
                        "></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:22pt;\"><br /></p></body></html>", None))
        self.Login_Button.setText(QCoreApplication.translate("MainWindow", u"Login", None))
        self.offboardButton.setText(QCoreApplication.translate("MainWindow", u"OffBoard", None))
        self.armButton.setText(QCoreApplication.translate("MainWindow", u"Arming", None))
        self.offboardLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.armLabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.ackButton.setText(QCoreApplication.translate("MainWindow", u"Acknowledge Alarm", None))
        self.Home_Button.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.Main_Button.setText(QCoreApplication.translate("MainWindow", u"Main", None))
        self.Alarm_Button.setText(QCoreApplication.translate("MainWindow", u"Alarms", None))
        self.Settings_Button.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.Map_Button.setText(QCoreApplication.translate("MainWindow", u"Map", None))
        self.labelTime.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.labelBattery.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.alarmIcon.setText("")
        self.labelControlMode.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.labelTimeRemaingBattery.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

