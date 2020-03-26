# -*- coding: utf-8 -*-
########################################################################
# Filename    : Main.py
# Description : This is the Freenove Three-wheeled Smart Car for Raspberry Pi the Server code.
#               Execute this file with Python3.
# auther      : www.freenove.com
# modification: 2020/03/26
########################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsScene)

from Camera_Server import *
from mTCPServer import mTCPServer
from Ui_Car_Server import Ui_MainWindow

from CloseThreading import stop_thread
import threading
import os
import sys,getopt
import time


class Main(QMainWindow, Ui_MainWindow):
    tcp = mTCPServer()
    tcp.setDaemon(True)
    cmr_Thread = Camera_Server()
    #cmr_Thread.setDaemon(True)
    #cmr_Thread = Camera_Server()
    user_ui = True
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.loadLogo()
        self.parseOpt()
        
    def parseOpt(self):
        try:
            self.opts,self.args = getopt.getopt(sys.argv[1:],"mnt")   
        except getopt.GetoptError as err: 
            print(str(err))
            return
        for o,a in self.opts:
            if o in ("-m"):             
                self.cmr_Thread = Camera_Server()
                self.cmr_Thread.start()
                self.btn_CameraServer.setText("TURN OFF")
            elif o in ("-t"):   
                self.tcp = mTCPServer()
                self.tcp.setDaemon(True)
                self.tcp.start()
                self.btn_TCPServer.setText("TURN OFF")
            elif o in ("-n"):
                self.user_ui = False
                
    def loadLogo(self):
        scene = QGraphicsScene (self)
        pic = QPixmap(":imgs/logo_Nomal")
        scene.addPixmap(pic)
        view = self.logo
        view.setStyleSheet("background:transparent")
        view.setScene(scene)
        view.setRenderHint(QPainter.Antialiasing)
       
    @pyqtSlot()
    def on_btn_CameraServer_clicked(self):
        print("btn_CameraServer Clicked!")
        if self.btn_CameraServer.text() == "TURN ON":
            self.btn_CameraServer.setText("TURN OFF")            
            self.cmr_Thread = Camera_Server()
            self.cmr_Thread.start()
        elif self.btn_CameraServer.text() == "TURN OFF":            
            self.btn_CameraServer.setText("TURN ON")
            t_Stop_Camera_Server = Stop_Camera_Server()
            t_Stop_Camera_Server.start()
    
    @pyqtSlot()
    def on_btn_TCPServer_clicked(self):
        if self.btn_TCPServer.text() == "TURN ON":
            self.btn_TCPServer.setText("TURN OFF")
            self.tcp = mTCPServer()
            self.tcp.setDaemon(True)
            self.tcp.start()
            
        elif self.btn_TCPServer.text() == "TURN OFF":
            self.btn_TCPServer.setText("TURN ON")
            print("Stop TCP Server Thread...")
            self.tcp.stopTCPServer()
            stop_thread(self.tcp)
    def closeEvent(self,event):
        QCoreApplication.instance().quit()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = Main()
    if dlg.user_ui == True:
        dlg.show()
        sys.exit(app.exec_())
    else :
        while True:
            time.sleep(1000)
        
    
