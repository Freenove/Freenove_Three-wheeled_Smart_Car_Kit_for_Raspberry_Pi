# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\Freenove\RaspberryPi\RaspberryPi Car\Python\PyQt_Test_Python3\Message.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(277, 125)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/imgs/logo_Mini"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(True)
        self.btn_OK = QtWidgets.QPushButton(Dialog)
        self.btn_OK.setGeometry(QtCore.QRect(100, 90, 75, 23))
        self.btn_OK.setObjectName("btn_OK")
        self.msg_Label = QtWidgets.QLabel(Dialog)
        self.msg_Label.setGeometry(QtCore.QRect(30, 20, 221, 41))
        self.msg_Label.setTextFormat(QtCore.Qt.AutoText)
        self.msg_Label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.msg_Label.setWordWrap(True)
        self.msg_Label.setObjectName("msg_Label")

        self.retranslateUi(Dialog)
        self.btn_OK.clicked.connect(Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Message"))
        self.btn_OK.setText(_translate("Dialog", "OK"))
        self.msg_Label.setText(_translate("Dialog", "TextLabel"))
import fn_logo_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
