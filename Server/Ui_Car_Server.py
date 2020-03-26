# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\Freenove\RaspberryPi\RaspberryPi Car\Python\Car_Server_Python3\Car_Server.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(340, 280)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/imgs/logo_Mini"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.btn_CameraServer = QtWidgets.QPushButton(self.centralWidget)
        self.btn_CameraServer.setGeometry(QtCore.QRect(180, 200, 71, 23))
        self.btn_CameraServer.setObjectName("btn_CameraServer")
        self.label_CamerServer = QtWidgets.QLabel(self.centralWidget)
        self.label_CamerServer.setGeometry(QtCore.QRect(60, 200, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_CamerServer.setFont(font)
        self.label_CamerServer.setObjectName("label_CamerServer")
        self.label_TCPServer = QtWidgets.QLabel(self.centralWidget)
        self.label_TCPServer.setGeometry(QtCore.QRect(80, 240, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_TCPServer.setFont(font)
        self.label_TCPServer.setObjectName("label_TCPServer")
        self.btn_TCPServer = QtWidgets.QPushButton(self.centralWidget)
        self.btn_TCPServer.setGeometry(QtCore.QRect(180, 240, 71, 23))
        self.btn_TCPServer.setObjectName("btn_TCPServer")
        self.logo = QtWidgets.QGraphicsView(self.centralWidget)
        self.logo.setGeometry(QtCore.QRect(10, 10, 320, 180))
        self.logo.setFocusPolicy(QtCore.Qt.NoFocus)
        self.logo.setAutoFillBackground(False)
        self.logo.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.logo.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.logo.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.logo.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.logo.setBackgroundBrush(brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.NoBrush)
        self.logo.setForegroundBrush(brush)
        self.logo.setObjectName("logo")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Freenove Server for Smart Car"))
        self.btn_CameraServer.setText(_translate("MainWindow", "TURN ON"))
        self.label_CamerServer.setText(_translate("MainWindow", "Camera Server"))
        self.label_TCPServer.setText(_translate("MainWindow", "TCP Server"))
        self.btn_TCPServer.setText(_translate("MainWindow", "TURN ON"))
import fn_logo_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
