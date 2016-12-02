# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\Freenove\RaspberryPi\RaspberryPi Car\Python\PyQt_Test\Message.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(277, 125)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/logo_Mini")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(True)
        self.btn_OK = QtGui.QPushButton(Dialog)
        self.btn_OK.setGeometry(QtCore.QRect(100, 90, 75, 23))
        self.btn_OK.setObjectName(_fromUtf8("btn_OK"))
        self.msg_Label = QtGui.QLabel(Dialog)
        self.msg_Label.setGeometry(QtCore.QRect(30, 20, 221, 41))
        self.msg_Label.setTextFormat(QtCore.Qt.AutoText)
        self.msg_Label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.msg_Label.setWordWrap(True)
        self.msg_Label.setObjectName(_fromUtf8("msg_Label"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.btn_OK, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Message", None))
        self.btn_OK.setText(_translate("Dialog", "OK", None))
        self.msg_Label.setText(_translate("Dialog", "TextLabel", None))

import fn_logo_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

