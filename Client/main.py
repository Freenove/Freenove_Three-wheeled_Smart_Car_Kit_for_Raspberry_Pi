# -*- coding: utf-8 -*-
"""
 ******************************************************************************
 * File  main.py
 * Author  Freenove (http://www.freenove.com)
 * Date    2016/11/14
 ******************************************************************************
 * Brief
 *   This is the Freenove Three-wheeled Smart Car for Raspberry Pi the Client code.
 *   Execute this file with Python2.7.
 ******************************************************************************
 * Copyright
 *   Copyright © Freenove (http://www.freenove.com)
 * License
 *   Creative Commons Attribution ShareAlike 3.0 
 *   (http://creativecommons.org/licenses/by-sa/3.0/legalcode)
 ******************************************************************************
"""
"""
Module implementing DemoClass.
"""
from PyQt4.QtCore import *
from PyQt4 import  QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import (QApplication, QMainWindow, QGraphicsScene)

from Ui_main import Ui_MainWindow
from TCPClient import TCPClient
from Command import COMMAND as cmd
from Message import Messgae_Dialog

from Freenove_Math import * 
import time
import threading
import math
#import copy
from CloseThreading import *

class DemoClass(QMainWindow, Ui_MainWindow):
    tcp = TCPClient()
    default_Server_IP = "192.168.1.108"
    Camera_H_Pos = 90
    Camera_V_Pos = 90
    SERVO_MIN_ANGLE = 0
    SERVO_MAX_ANGLE = 180
    Is_Paint_Thread_On = False
    global t_Paint_Thread
    sonic_Index = 0
    sonic_buff = [0]*20
    send_Counter = 0
    Is_tcp_Idle = True
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.msgDlg = Messgae_Dialog()
        self.loadLogo()
        #self.webView.setZoomFactor(1.0)
        self.webView.setUrl(QUrl("html/car_photo.html"))
        self.webView.page().mainFrame().setScrollBarPolicy(Qt.Horizontal, Qt.ScrollBarAlwaysOff)
        self.webView.page().mainFrame().setScrollBarPolicy(Qt.Vertical, Qt.ScrollBarAlwaysOff) 
        try :            
            file_Config = open("Config.txt", "r")
            self.default_Server_IP = file_Config.read()
        except Exception, e:
            print "Config.txt is not exist,If the Program is the first executed, To ignore this information", e
        finally:
            file_Config.close()
        self.lineEdit_IP_Addr.setText(self.default_Server_IP) 
        
        self.wgt_Drawing = PaintArea(self)
        self.wgt_Drawing.setGeometry(10,10,400,300)
        self.wgt_Drawing.setVisible(False)
        self.mutex = threading.Lock()  
        #self.t_Recv_Sonic_Thread = Recv_Sonic_Thread(self)
        #self.t_Scan_Sonic_Thread = Scan_Sonic_Thread(self)
        #self.t_Paint_Thread = Piant_Thread(self.wgt_Drawing)
        #self.t_Paint_Thread.start()
        
    def loadLogo(self):
        scene = QGraphicsScene (self)
        #scene.setSceneRect(-600, -600, 1200, 1200) 
        #pic = QPixmap("imgs/logo02.png")
        pic = QPixmap(":/imgs/logo_Nomal")
        scene.addPixmap(pic)
        view = self.logo
        view.setStyleSheet("background:transparent")
        view.setScene(scene)
        view.setRenderHint(QPainter.Antialiasing)
        view.show()
   
    @pyqtSignature("")
    def on_btn_Up_pressed(self):        
        self.Camera_V_Pos = self.Camera_V_Pos + self.slider_Camera.value()
        self.Camera_V_Pos = constrain(self.Camera_V_Pos, self.SERVO_MIN_ANGLE, self.SERVO_MAX_ANGLE)
        self.slider_Camera_V.setValue(self.Camera_V_Pos)
        self.tcp.sendData(cmd.CMD_CAMERA_UP + str(self.Camera_V_Pos))
    
    @pyqtSignature("")
    def on_btn_Up_released(self):
        self.tcp.sendData(cmd.CMD_CAMERA_STOP)
    
    @pyqtSignature("")
    def on_btn_Left_pressed(self):
        self.Camera_H_Pos = self.Camera_H_Pos + self.slider_Camera.value()
        self.Camera_H_Pos = constrain(self.Camera_H_Pos, self.SERVO_MIN_ANGLE, self.SERVO_MAX_ANGLE)
        self.slider_Camera_H.setValue(self.Camera_H_Pos)
        self.tcp.sendData(cmd.CMD_CAMERA_LEFT + str(self.Camera_H_Pos))        
    
    @pyqtSignature("")
    def on_btn_Left_released(self):
        self.tcp.sendData(cmd.CMD_CAMERA_STOP)
    
    @pyqtSignature("")
    def on_btn_Down_pressed(self):
        self.Camera_V_Pos = self.Camera_V_Pos - self.slider_Camera.value()
        self.Camera_V_Pos = constrain(self.Camera_V_Pos, 80, self.SERVO_MAX_ANGLE)
        self.slider_Camera_V.setValue(self.Camera_V_Pos)
        self.tcp.sendData(cmd.CMD_CAMERA_DOWN + str(self.Camera_V_Pos))        
    
    @pyqtSignature("")
    def on_btn_Down_released(self):
        self.tcp.sendData(cmd.CMD_CAMERA_STOP)
    
    @pyqtSignature("")
    def on_btn_Right_pressed(self):
        self.Camera_H_Pos = self.Camera_H_Pos - self.slider_Camera.value()
        self.Camera_H_Pos = constrain(self.Camera_H_Pos, self.SERVO_MIN_ANGLE, self.SERVO_MAX_ANGLE)
        self.slider_Camera_H.setValue(self.Camera_H_Pos)
        self.tcp.sendData(cmd.CMD_CAMERA_LEFT + str(self.Camera_H_Pos))
    
    @pyqtSignature("")
    def on_btn_Right_released(self):
        self.tcp.sendData(cmd.CMD_CAMERA_STOP)
    
    @pyqtSignature("")
    def on_btn_Home_clicked(self):
        self.Camera_H_Pos = 90
        self.Camera_V_Pos = 90
        self.slider_Camera_H.setValue(self.Camera_H_Pos)
        self.slider_Camera_V.setValue(self.Camera_V_Pos)
        self.tcp.sendData(cmd.CMD_CAMERA_LEFT + str(90+self.slider_FineServo2.value()))
        self.tcp.sendData(cmd.CMD_CAMERA_UP + str(90+self.slider_FineServo2.value()))
        
    @pyqtSignature("")
    def on_btn_Forward_pressed(self):
        #self.tcp.sendData(cmd.CMD_FORWARD + str(self.slider_Speed.value()))
        self.setMoveSpeed(cmd.CMD_FORWARD,self.slider_Speed.value())
    
    @pyqtSignature("")
    def on_btn_Forward_released(self):
        self.tcp.sendData(cmd.CMD_STOP)
    
    @pyqtSignature("")
    def on_btn_TurnLeft_pressed(self):
        self.tcp.sendData(cmd.CMD_TURN_LEFT + str(self.slider_Direction.value() + self.slider_FineServo1.value()))
    
    @pyqtSignature("")
    def on_btn_TurnLeft_released(self):
        self.tcp.sendData(cmd.CMD_TURN_CENTER + str(90+self.slider_FineServo1.value()))
    
    @pyqtSignature("")
    def on_btn_TurnRight_pressed(self):
        self.tcp.sendData(cmd.CMD_TURN_RIGHT + str(self.slider_Direction.value() + self.slider_FineServo1.value()))
    
    @pyqtSignature("")
    def on_btn_TurnRight_released(self):
        self.tcp.sendData(cmd.CMD_TURN_CENTER + str(90+self.slider_FineServo1.value()))
    
    @pyqtSignature("")
    def on_btn_Backward_pressed(self):
        #self.tcp.sendData(cmd.CMD_BACKWARD + str(self.slider_Speed.value()))
        self.setMoveSpeed(cmd.CMD_BACKWARD,self.slider_Speed.value())
    
    @pyqtSignature("")
    def on_btn_Backward_released(self):
        self.tcp.sendData(cmd.CMD_STOP)

    @pyqtSignature("")
    def on_btn_Mode_clicked(self):
        if self.btn_Mode.text() == "VIDEO":            
            self.webView.setVisible(False)
            self.wgt_Drawing.setVisible(True)
            if self.btn_Connect.text() == "DisConnect":
                self.t_Paint_Thread = Piant_Thread(self)
                self.t_Paint_Thread.start()
                self.t_Recv_Sonic_Thread = Recv_Sonic_Thread(self)
                self.t_Recv_Sonic_Thread.start()
                self.t_Scan_Sonic_Thread = Scan_Sonic_Thread(self)
                self.t_Scan_Sonic_Thread.start()
                self.Is_Paint_Thread_On = True
            self.btn_Mode.setText("RADAR")
        elif self.btn_Mode.text() == "RADAR":            
            self.wgt_Drawing.setVisible(False)
            self.webView.setVisible(True)          
            if self.Is_Paint_Thread_On == True:    
                if self.t_Paint_Thread.is_alive():                    
                    #stop_thread(self.t_Paint_Thread)
                    self.t_Paint_Thread.isRun = False
                    print "Stop_thread ... -> t_Paint_Thread", self.t_Paint_Thread.getName()                
                if self.t_Recv_Sonic_Thread.is_alive():
                    #stop_thread(self.t_Recv_Sonic_Thread)
                    self.t_Recv_Sonic_Thread.isRun = False
                    print "Stop_thread ... -> t_Recv_Sonic_Thread", self.t_Recv_Sonic_Thread.getName()
                if self.t_Scan_Sonic_Thread.is_alive():
                    #stop_thread(self.t_Scan_Sonic_Thread)
                    self.t_Scan_Sonic_Thread.isRun = False
                    print "Stop_thread ... -> t_Scan_Sonic_Thread", self.t_Scan_Sonic_Thread.getName()
                self.Is_Paint_Thread_On = False
            self.btn_Mode.setText("VIDEO")
        
    @pyqtSignature("")
    def on_btn_Connect_clicked(self):
        if self.btn_Connect.text() == "Connect":
            server_ip = self.lineEdit_IP_Addr.text()
            print "Connecting......", server_ip                
            try:
                self.tcp.connectToServer(address = (server_ip, 12345))
            except Exception, e:
                print "Connect to server Faild!: Server IP is right? Server is opend?", e                
                self.msgDlg.showMessage("Connect to server Faild! \n\t1. Server IP is right? \n\t2. Server is opend?")
                return 
            print "Connecttion Successful !"
            if self.default_Server_IP != server_ip :
                file_Config = open("Config.txt", "w")
                file_Config.write(server_ip)
                file_Config.close()
                print "default_Server_IP is Changed!"
            self.webView.setZoomFactor(1.2)
            self.webView.setUrl(QUrl("http://"+server_ip+":8090/javascript_simple.html"))
            
            #wbv_Scale = 1.2
            #self.webView.resize(400, 300)
            #self.webView.setZoomFactor(wbv_Scale)            
            self.lineEdit_IP_Addr.setEnabled(False)
            self.btn_Connect.setText( "DisConnect")
        elif self.btn_Connect.text() == "DisConnect":
            self.tcp.disConnect()
            self.webView.setContentsMargins(80, -8, 0, 0)
            self.webView.setUrl(QUrl("html/car_photo.html"))
            self.lineEdit_IP_Addr.setEnabled(True)
            self.btn_Connect.setText( "Connect")
    
    def keyPressEvent(self,event):  
        if event.key() == Qt.Key_Up:
            self.Camera_V_Pos = self.Camera_V_Pos + self.slider_Camera.value() + self.slider_FineServo3.value()
            self.Camera_V_Pos = constrain(self.Camera_V_Pos, self.SERVO_MIN_ANGLE, self.SERVO_MAX_ANGLE)
            self.slider_Camera_V.setValue(self.Camera_V_Pos)
            self.tcp.sendData(cmd.CMD_CAMERA_UP + str(self.Camera_V_Pos))
            
            self.wgt_Drawing.max_range = self.Camera_V_Pos
            self.wgt_Drawing.repaint()
        elif event.key() == Qt.Key_Down:
            self.Camera_V_Pos = self.Camera_V_Pos - self.slider_Camera.value() + self.slider_FineServo3.value()
            self.Camera_V_Pos = constrain(self.Camera_V_Pos, 80, self.SERVO_MAX_ANGLE)
            self.slider_Camera_V.setValue(self.Camera_V_Pos)
            self.tcp.sendData(cmd.CMD_CAMERA_DOWN + str(self.Camera_V_Pos))
            
            self.wgt_Drawing.max_range = self.Camera_V_Pos
            self.wgt_Drawing.repaint()
        elif event.key() == Qt.Key_Left:
            self.Camera_H_Pos = self.Camera_H_Pos + self.slider_Camera.value() + self.slider_FineServo2.value()
            self.Camera_H_Pos = constrain(self.Camera_H_Pos, self.SERVO_MIN_ANGLE, self.SERVO_MAX_ANGLE)
            self.slider_Camera_H.setValue(self.Camera_H_Pos)
            self.tcp.sendData(cmd.CMD_CAMERA_LEFT + str(self.Camera_H_Pos))
        elif event.key() == Qt.Key_Right:
            self.Camera_H_Pos = self.Camera_H_Pos - self.slider_Camera.value() + self.slider_FineServo2.value()
            self.Camera_H_Pos = constrain(self.Camera_H_Pos, self.SERVO_MIN_ANGLE, self.SERVO_MAX_ANGLE)
            self.slider_Camera_H.setValue(self.Camera_H_Pos)
            self.tcp.sendData(cmd.CMD_CAMERA_LEFT + str(self.Camera_H_Pos))
        elif event.key() == Qt.Key_R:
            self.tcp.sendData(cmd.CMD_RGB_R)
        elif event.key() == Qt.Key_G:
            self.tcp.sendData(cmd.CMD_RGB_G)
        elif event.key() == Qt.Key_B:
            self.tcp.sendData(cmd.CMD_RGB_B)
        elif event.key() == Qt.Key_H:
            self.Camera_H_Pos = 90
            self.Camera_V_Pos = 90
            self.slider_Camera_H.setValue(self.Camera_H_Pos)
            self.slider_Camera_V.setValue(self.Camera_V_Pos)
            self.tcp.sendData(cmd.CMD_CAMERA_LEFT + str(90+self.slider_FineServo2.value()))
            self.tcp.sendData(cmd.CMD_CAMERA_UP + str(90+self.slider_FineServo2.value()))
            
        if event.isAutoRepeat():
            pass
        else :
            #print "You Pressed Key : ", event.key(), event.text() 
            if event.key() == Qt.Key_W:
                self.setMoveSpeed(cmd.CMD_FORWARD,self.slider_Speed.value())
            elif event.key() == Qt.Key_S:
                self.setMoveSpeed(cmd.CMD_BACKWARD,self.slider_Speed.value())
            elif event.key() == Qt.Key_A:
                self.tcp.sendData(cmd.CMD_TURN_LEFT + str(self.slider_Direction.value() + self.slider_FineServo1.value()))
            elif event.key() == Qt.Key_D:                  
                self.tcp.sendData(cmd.CMD_TURN_RIGHT + str(self.slider_Direction.value() + self.slider_FineServo1.value()))  
            elif event.key() == Qt.Key_V:
                self.tcp.sendData(cmd.CMD_BUZZER_ALARM)                
                
    def keyReleaseEvent (self, event):
        if event.isAutoRepeat():
            pass
        else:
            #print "You Released Key : ", event.key()
            if event.key() == Qt.Key_W or event.key() == Qt.Key_S :
                self.tcp.sendData(cmd.CMD_STOP)
            elif event.key() == Qt.Key_A or event.key() == Qt.Key_D:
                self.tcp.sendData(cmd.CMD_TURN_CENTER + str(90+self.slider_FineServo1.value()))
            elif event.key() == Qt.Key_V:
                self.tcp.sendData(cmd.CMD_BUZZER_ALARM)
        if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down or event.key() == Qt.Key_Left or event.key() == Qt.Key_Right:
            self.tcp.sendData(cmd.CMD_CAMERA_STOP)
    
    def setMoveSpeed(self, CMD, spd):
        self.tcp.sendData(CMD + str(spd/3))
        time.sleep(0.07)
        self.tcp.sendData(CMD + str(spd/3*2))
        time.sleep(0.07)
        self.tcp.sendData(CMD + str(spd))
    @pyqtSignature("int")
    def on_slider_Camera_valueChanged(self, value):
        self.tcp.sendData(cmd.CMD_CAMERA_SLIDER + str(value))
    
    @pyqtSignature("int")
    def on_slider_Speed_valueChanged(self, value):
        pass
        #self.tcp.sendData(cmd.CMD_SPEED_SLIDER + str(value))
    
    @pyqtSignature("int")
    def on_slider_Direction_valueChanged(self, value):
        pass
        #self.tcp.sendData(cmd.CMD_DIR_SLIDER + str(value))
    @pyqtSignature("")
    def on_btn_RGB_R_clicked(self):
        self.tcp.sendData(cmd.CMD_RGB_R)    
    @pyqtSignature("")
    def on_btn_RGB_G_clicked(self):
        self.tcp.sendData(cmd.CMD_RGB_G)    
    @pyqtSignature("")
    def on_btn_RGB_B_clicked(self):
        self.tcp.sendData(cmd.CMD_RGB_B)
    @pyqtSignature("")
    def on_btn_Buzzer_clicked(self):
        pass
        #self.tcp.sendData(cmd.CMD_BUZZER_ALARM)        
    @pyqtSignature("")
    def on_btn_Buzzer_pressed(self):
        self.tcp.sendData(cmd.CMD_BUZZER_ALARM)        
    
    @pyqtSignature("")
    def on_btn_Buzzer_released(self):
        self.tcp.sendData(cmd.CMD_BUZZER_ALARM)        
     
class Recv_Sonic_Thread(threading.Thread):
    def __init__(self, widget):
        super(Recv_Sonic_Thread, self).__init__()
        self.wgt_main = widget
        self.isRun = True
    
    def run(self):
        #while True:
        while self.isRun:
            sonic = self.wgt_main.tcp.recvData()
            try :
                iSonic = float(sonic)
            except Exception, e:
                print "Sonic Data error :", e
                iSonic = 0
            self.wgt_main.sonic_buff[self.wgt_main.sonic_Index] = iSonic
            #print iSonic  

class Scan_Sonic_Thread(threading.Thread):
    def __init__(self, widget):
        super(Scan_Sonic_Thread, self).__init__()
        self.wgt_main = widget
        self.isRun = True
    def run(self):
        #while True:
        while self.isRun:
            self.scan_Sonic()
            #time.sleep(0.1)
            
    def scan_Sonic(self):
        self.min_Angle = 45
        self.max_Angle = 135
        self.inteval_Angle = 10
        self.scan_speed = 0.05
        #print "scan Sonic...."
        for angle in range(self.min_Angle, self.max_Angle+1, self.inteval_Angle):
            self.wgt_main.sonic_Index = angle/self.inteval_Angle
            self.wgt_main.Camera_H_Pos = angle
            self.wgt_main.slider_Camera_H.setValue(self.wgt_main.Camera_H_Pos)
            if self.wgt_main.mutex.acquire():
                self.wgt_main.tcp.sendData(cmd.CMD_SONIC_LEFT+str(self.wgt_main.Camera_H_Pos))  
                self.wgt_main.tcp.sendData(cmd.CMD_ULTRASONIC)
                self.wgt_main.mutex.release()
            time.sleep(self.scan_speed)        
        print self.wgt_main.sonic_buff
        for angle in range(self.max_Angle, self.min_Angle-1, -1*self.inteval_Angle):
            self.wgt_main.sonic_Index = angle/self.inteval_Angle
            self.wgt_main.Camera_H_Pos = angle
            self.wgt_main.slider_Camera_H.setValue(self.wgt_main.Camera_H_Pos)
            if self.wgt_main.mutex.acquire():
                self.wgt_main.tcp.sendData(cmd.CMD_SONIC_LEFT+str(self.wgt_main.Camera_H_Pos))  
                self.wgt_main.tcp.sendData(cmd.CMD_ULTRASONIC)
                self.wgt_main.mutex.release()
            time.sleep(self.scan_speed)
        print self.wgt_main.sonic_buff  
        
class Piant_Thread(threading.Thread):
    #wgt_Drawing = PaintArea(QMainWindow)
    def __init__(self, widget):
        super(Piant_Thread, self).__init__()
        self.wgt_main = widget
        self.wgtDrawing = widget.wgt_Drawing       
        self.isRun = True 
    def run(self):
        #while True:
        while self.isRun:
            #print "Piant_Thread", self.getName()
            self.wgtDrawing.update()
            time.sleep(0.05)
    def scan_Sonic(self):
        self.min_Angle = 45
        self.max_Angle = 135
        self.inteval_Angle = 10
        #print "scan Sonic...."
        for angle in range(self.min_Angle, self.max_Angle+1, self.inteval_Angle):
            self.wgt_main.sonic_Index = angle/self.inteval_Angle
            self.wgt_main.Camera_H_Pos = angle
            self.wgt_main.slider_Camera_H.setValue(self.wgt_main.Camera_H_Pos)
            if self.wgt_main.mutex.acquire():
                self.wgt_main.tcp.sendData(cmd.CMD_SONIC_LEFT+str(self.wgt_main.Camera_H_Pos))  
                self.wgt_main.tcp.sendData(cmd.CMD_ULTRASONIC)
                self.wgt_main.mutex.release()
            #self.wgt_main.sonic_buff[angle/self.inteval_Angle] = iSonic            
            time.sleep(0.1)        
        #send_Counter = send_Counter +1
        print self.wgt_main.sonic_buff
        for angle in range(self.max_Angle, self.min_Angle-1, -1*self.inteval_Angle):
            self.wgt_main.sonic_Index = angle/self.inteval_Angle
            self.wgt_main.Camera_H_Pos = angle
            self.wgt_main.slider_Camera_H.setValue(self.wgt_main.Camera_H_Pos)
            if self.wgt_main.mutex.acquire():
                self.wgt_main.tcp.sendData(cmd.CMD_SONIC_LEFT+str(self.wgt_main.Camera_H_Pos))  
                self.wgt_main.tcp.sendData(cmd.CMD_ULTRASONIC)
                self.wgt_main.mutex.release()
            #self.wgt_main.sonic_buff[angle/self.inteval_Angle] = iSonic
            time.sleep(0.1)
        print self.wgt_main.sonic_buff    
class PaintArea(QWidget):    
    max_range = 201
    def __init__(self, parent=None):
        super(PaintArea,self).__init__(parent)
        self.parent = parent
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(192, 192, 192))
        self.setPalette(palette)
        
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.coordinate_system(qp)
        qp.end()
        
    def coordinate_system(self,  qp):
        qp.setPen(QtCore.Qt.red)
        size = self.size()        
        #qp.drawRect(60, 60, 100, 100)
        orgin_X = size.width()/2.0
        orgin_Y = size.height()-100
        qp.drawLine(0, orgin_Y, size.width(),orgin_Y )
        qp.drawLine(orgin_X, 0, orgin_X,size.height())
        #print time.ctime(),"refrash....."
        for r in range(20, self.max_range, 20):
            r = constrain(r, 0, 200)
            qp.drawArc(orgin_X-r,orgin_Y-r, 2*r, 2*r, 0, 180*16)
            #qp.drawText(orgin_X+r,orgin_Y+10, str(r))
            #qp.drawText(orgin_X-r,orgin_Y+10, str(r))
        qp.setPen(QtCore.Qt.black)
        qp.setBrush(QtCore.Qt.black)
        qp.drawEllipse(orgin_X-5, orgin_Y-5, 10, 10)
        for i in range (0, 10, 1):
            d = self.parent.sonic_buff[i+4]
            min_Angle = 45#self.parent.min_Angle
            if d != 0:
                qp.drawEllipse(orgin_X + 2*d*math.cos((min_Angle+i*10)/180.0*math.pi), orgin_Y - 2*d*math.sin((min_Angle+i*10)/180.0*math.pi), 5, 5)
        #for target_cycle in 
            
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dlg = DemoClass()
    dlg.show()
    sys.exit(app.exec_())
    

