# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/pi/Smart_Car/Car_Server/Car_Server.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(340, 280)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/logo_Mini")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.btn_CameraServer = QtGui.QPushButton(self.centralWidget)
        self.btn_CameraServer.setGeometry(QtCore.QRect(180, 200, 71, 23))
        self.btn_CameraServer.setObjectName(_fromUtf8("btn_CameraServer"))
        self.label_CamerServer = QtGui.QLabel(self.centralWidget)
        self.label_CamerServer.setGeometry(QtCore.QRect(60, 200, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_CamerServer.setFont(font)
        self.label_CamerServer.setObjectName(_fromUtf8("label_CamerServer"))
        self.label_TCPServer = QtGui.QLabel(self.centralWidget)
        self.label_TCPServer.setGeometry(QtCore.QRect(80, 240, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_TCPServer.setFont(font)
        self.label_TCPServer.setObjectName(_fromUtf8("label_TCPServer"))
        self.btn_TCPServer = QtGui.QPushButton(self.centralWidget)
        self.btn_TCPServer.setGeometry(QtCore.QRect(180, 240, 71, 23))
        self.btn_TCPServer.setObjectName(_fromUtf8("btn_TCPServer"))
        self.logo = QtGui.QGraphicsView(self.centralWidget)
        self.logo.setGeometry(QtCore.QRect(10, 10, 320, 180))
        self.logo.setFocusPolicy(QtCore.Qt.NoFocus)
        self.logo.setAutoFillBackground(False)
        self.logo.setFrameShape(QtGui.QFrame.NoFrame)
        self.logo.setFrameShadow(QtGui.QFrame.Sunken)
        self.logo.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.logo.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.logo.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.logo.setForegroundBrush(brush)
        self.logo.setObjectName(_fromUtf8("logo"))
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Freenove Server for Smart Car", None))
        self.btn_CameraServer.setText(_translate("MainWindow", "TURN ON", None))
        self.label_CamerServer.setText(_translate("MainWindow", "Camera Server", None))
        self.label_TCPServer.setText(_translate("MainWindow", "TCP Server", None))
        self.btn_TCPServer.setText(_translate("MainWindow", "TURN ON", None))

import fn_logo_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

