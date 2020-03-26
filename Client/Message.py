# -*- coding: utf-8 -*-
########################################################################
# Filename    : Message.py
# Description : This is the Class Messgae_Dialog code .
# auther      : www.freenove.com
# modification: 2020/03/26
########################################################################

# from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets  import QDialog

from Ui_Message import Ui_Dialog


class Messgae_Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)        
        #self.messageDlg=QDialog()
        #self.messageUI = Ui_Dialog()
        #self.messageUI.setupUi(self.messageDlg)
        
    def showMessage(self, txt):        
        self.msg_Label.setText(txt)
        self.show()
        #self.messageUI.msg_Label.setText(txt)
        #self.messageDlg.show()
