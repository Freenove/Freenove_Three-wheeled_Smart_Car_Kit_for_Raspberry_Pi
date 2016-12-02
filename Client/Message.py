# -*- coding: utf-8 -*-
"""
 ******************************************************************************
 * File  Message.py
 * Author  Freenove (http://www.freenove.com)
 * Date    2016/11/14
 ******************************************************************************
 * Brief
 *   This is the Class Messgae_Dialog code .
 ******************************************************************************
 * Copyright
 *   Copyright © Freenove (http://www.freenove.com)
 * License
 *   Creative Commons Attribution ShareAlike 3.0 
 *   (http://creativecommons.org/licenses/by-sa/3.0/legalcode)
 ******************************************************************************
"""
"""
Module implementing Messgae_Dialog.
"""

from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QDialog

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
