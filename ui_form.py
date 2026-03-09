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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStackedWidget,
    QStatusBar, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1313, 763)
        self.widget = QWidget(MainWindow)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"color: rgb(26, 95, 180);\n"
"background-color: rgb(0, 0, 0);")
        self.stackedWidget = QStackedWidget(self.widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(100, 0, 1291, 781))
        self.Main_pg = QWidget()
        self.Main_pg.setObjectName(u"Main_pg")
        self.Main_pg.setStyleSheet(u"background-color: rgb(255, 255, 255);\n"
"background-color: rgb(255, 163, 72);")
        self.videoLabel = QLabel(self.Main_pg)
        self.videoLabel.setObjectName(u"videoLabel")
        self.videoLabel.setGeometry(QRect(530, 110, 431, 271))
        self.toggleInputButton = QPushButton(self.Main_pg)
        self.toggleInputButton.setObjectName(u"toggleInputButton")
        self.toggleInputButton.setGeometry(QRect(250, 580, 201, 121))
        self.toggleInputButton.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color: rgb(245, 194, 17);")
        self.verticalLayoutWidget = QWidget(self.Main_pg)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(40, 100, 431, 281))
        self.videoLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.videoLayout.setObjectName(u"videoLayout")
        self.videoLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget.addWidget(self.Main_pg)
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
        self.stackedWidget.addWidget(self.Home_pg)
        self.Alarm_pg = QWidget()
        self.Alarm_pg.setObjectName(u"Alarm_pg")
        self.Alarm_pg.setStyleSheet(u"background-color: rgb(153, 193, 241);")
        self.stackedWidget.addWidget(self.Alarm_pg)
        self.sidebarWidget = QWidget(self.widget)
        self.sidebarWidget.setObjectName(u"sidebarWidget")
        self.sidebarWidget.setGeometry(QRect(0, 70, 91, 921))
        self.Home_Button = QPushButton(self.sidebarWidget)
        self.Home_Button.setObjectName(u"Home_Button")
        self.Home_Button.setGeometry(QRect(0, 0, 101, 61))
        self.Main_Button = QPushButton(self.sidebarWidget)
        self.Main_Button.setObjectName(u"Main_Button")
        self.Main_Button.setGeometry(QRect(0, 60, 101, 61))
        self.Alarm_Button = QPushButton(self.sidebarWidget)
        self.Alarm_Button.setObjectName(u"Alarm_Button")
        self.Alarm_Button.setGeometry(QRect(0, 120, 101, 61))
        self.Alarm_Button_2 = QPushButton(self.sidebarWidget)
        self.Alarm_Button_2.setObjectName(u"Alarm_Button_2")
        self.Alarm_Button_2.setGeometry(QRect(0, 180, 101, 61))
        self.Alarm_Button_3 = QPushButton(self.sidebarWidget)
        self.Alarm_Button_3.setObjectName(u"Alarm_Button_3")
        self.Alarm_Button_3.setGeometry(QRect(0, 240, 101, 61))
        self.statusWidget = QWidget(self.widget)
        self.statusWidget.setObjectName(u"statusWidget")
        self.statusWidget.setGeometry(QRect(0, -10, 1331, 80))
        self.statusWidget.setStyleSheet(u"background-color: rgb(192, 191, 188);")
        self.labelTime = QLabel(self.statusWidget)
        self.labelTime.setObjectName(u"labelTime")
        self.labelTime.setGeometry(QRect(170, 30, 421, 18))
        MainWindow.setCentralWidget(self.widget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1313, 23))
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
        self.Home_Button.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.Main_Button.setText(QCoreApplication.translate("MainWindow", u"Main", None))
        self.Alarm_Button.setText(QCoreApplication.translate("MainWindow", u"Alarms", None))
        self.Alarm_Button_2.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.Alarm_Button_3.setText(QCoreApplication.translate("MainWindow", u"Map", None))
        self.labelTime.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
    # retranslateUi

