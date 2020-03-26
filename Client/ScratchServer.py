# -*- coding: utf-8 -*-
########################################################################
# Filename    : ScratchServer.py
# Description : Module implementing Web Server Client for Scratch Extension.
# auther      : www.freenove.com
# modification: 2020/03/26
########################################################################


from PyQt5 import QtCore, QtGui  #, QtWebEngineWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QApplication, QMainWindow, QGraphicsScene, QWidget)

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from TCPClient import TCPClient
from Command import COMMAND as cmd
from Message import Messgae_Dialog

from Freenove_Math import * 
import time
import threading
import math
#import copy
from CloseThreading import *
import http.server, http.server
from http.server import HTTPServer, BaseHTTPRequestHandler

class ScratchServer(BaseHTTPRequestHandler):
    tcp = TCPClient()
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

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(self.parsePath(self.path).encode('utf-8'))

    def parsePath(self, path):
        pathParts = path.split('/')
        if len(pathParts) < 2:
            ScratchServer.lastError = "ERROR: No Command detected"
            return ScratchServer.lastError

        cmd = pathParts[1]

        if cmd == "favicon.ico": return
        
        if (cmd != "poll" and cmd != "lastError"): ScratchServer.lastError = ""

        if cmd == "crossdomain.xml":
            return self.getXDomainResponse()
        elif cmd == "connect":
            server_ip = pathParts[2]
            return self.connect2Car(server_ip)
        elif cmd == "disconnect":
            return self.disconnectFromCar()
        elif cmd == "cUp":
            return self.cameraUp(pathParts[2])
        elif cmd == "cDown":
            return self.cameraDown(pathParts[2])
        elif cmd == "cLeft":
            return self.cameraLeft(pathParts[2])
        elif cmd == "cRight":
            return self.cameraRight(pathParts[2])
        elif cmd == "centerCamera":
            return self.centerCamera()
        elif cmd == "moveForward":
            return self.moveForward(pathParts[2])
        elif cmd == "moveBackward":
            return self.moveBackward(pathParts[2])
        elif cmd == "stop":
            return self.stop()
        elif cmd == "stepForward":
            return self.stepForward(pathParts[2], pathParts[3])
        elif cmd == "stepBackward":
            return self.stepBackward(pathParts[2], pathParts[3])
        elif cmd == "turnLeft":
            return self.turnLeft(pathParts[2])
        elif cmd == "turnRight":
            return self.turnRight(pathParts[2])
        elif cmd == "center":
            return self.center();
        elif cmd == "lightRed":
            return self.lightRed()
        elif cmd == "lightGreen":
            return self.lightGreen()
        elif cmd == "lightBlue":
            return self.lightBlue()
        elif cmd == "buzz":
            return self.buzz(pathParts[2])
        elif cmd == "distance":
            return self.distance()
        elif cmd == "lastError":
            return self.getLastError()
        elif cmd == "lastMessage":
            return self.lastMessage()
        elif cmd == "poll":
            return self.poll()
        elif cmd == "reset_all":
            return self.resetAll()

        ScratchServer.lastError = "ERROR: '" + pathParts[1] + "' is not a valid command"
        return ScratchServer.lastError

    def lastMessage(self):
        print(ScratchServer.msg)
        return ScratchServer.msg

    def getLastError(self):
        print(ScratchServer.lastError)
        return ScratchServer.lastError

    def getXDomainResponse(self):
        resp = "<cross-domain-policy>\n"
        resp += "<allow-access-from domain=\"*\" to-ports=\"8085\"/>\n"
        resp += "</cross-domain-policy>\x00"
        return resp

    def poll(self):
        ScratchServer.msg = "sonic " + str(ScratchServer.iSonic)
        if ScratchServer.lastError != "": ScratchServer.msg += "\nERROR: " + ScratchServer.lastError
        print(ScratchServer.msg)
        return ScratchServer.msg

    
    def centerCamera(self):
        try:
            ScratchServer.Camera_V_Pos = 90
            ScratchServer.Camera_H_Pos = 90
            self.tcp.sendData(cmd.CMD_CAMERA_UP + str(ScratchServer.Camera_V_Pos))
            self.tcp.sendData(cmd.CMD_CAMERA_LEFT + str(ScratchServer.Camera_H_Pos))
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        return ""

    
    def resetAll(self):
        try:
            print("returning crossdomain.xml")
            self.centerCamera(0)
            self.stop()
            self.center(0)
            self.buzz(1000)
            return "Reset Complete"
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError


    
    def connect2Car(self, server_ip):
        print("Connecting......", server_ip) 
        try:
            self.tcp.connectToServer(address = (str(server_ip), 12345))
        except Exception as e:
            #print(type(server_ip),type(e))
            ScratchServer.lastError =  e#"Connect to server " + server_ip + " Failed!: " +
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        ScratchServer.msg = "Connection Successful !"
        print(ScratchServer.msg)
        return ScratchServer.msg

    
    def disconnectFromCar(self):
        try:
            self.tcp.disConnect()
            print("Disconnection Successful !")
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        ScratchServer.msg = "Disconnected"
        print(ScratchServer.msg)
        return ScratchServer.msg

    
    def distance(self):
        try:
            sonic = 0
            iTry = 0
            while sonic == 0 and iTry < 3:
                self.tcp.sendData(cmd.CMD_ULTRASONIC)
                sonic = self.tcp.recvData()
            ScratchServer.iSonic = float(sonic)
        except Exception as e:
            ScratchServer.msg = "Sonic Data error :\n" + e
            ScratchServer.lastError = ScratchServer.msg
            print(ScratchServer.msg)
            ScratchServer.iSonic = 0
            return ScratchServer.msg

        ScratchServer.msg = "distance received: " + str(ScratchServer.iSonic)
        print(ScratchServer.msg)
        return str(ScratchServer.iSonic)
   
    
    
    def cameraUp(self, angle):
        try:
            angle = int(angle)
            ScratchServer.Camera_V_Pos = 90 + angle
            ScratchServer.Camera_V_Pos = constrain(ScratchServer.Camera_V_Pos, self.SERVO_MIN_ANGLE, self.SERVO_MAX_ANGLE)
            self.tcp.sendData(cmd.CMD_CAMERA_UP + str(ScratchServer.Camera_V_Pos))
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        ScratchServer.msg = "Camera V moved up to " + str(ScratchServer.Camera_V_Pos)
        print(ScratchServer.msg)
        return ScratchServer.msg
   
    
    def cameraDown(self, angle):
        try:
            angle = int(angle)
            ScratchServer.Camera_V_Pos = 90 - angle
            ScratchServer.Camera_V_Pos = constrain(ScratchServer.Camera_V_Pos, 80, self.SERVO_MAX_ANGLE)
            self.tcp.sendData(cmd.CMD_CAMERA_DOWN + str(ScratchServer.Camera_V_Pos))        
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        ScratchServer.msg = "Camera V moved down to " + str(ScratchServer.Camera_V_Pos)
        print(ScratchServer.msg)
        return ScratchServer.msg

    
    def cameraLeft(self, angle):
        try:
            angle = int(angle)
            ScratchServer.Camera_H_Pos = 90 + angle
            ScratchServer.Camera_H_Pos = constrain(ScratchServer.Camera_H_Pos, self.SERVO_MIN_ANGLE, self.SERVO_MAX_ANGLE)
            self.tcp.sendData(cmd.CMD_CAMERA_LEFT + str(ScratchServer.Camera_H_Pos))
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        ScratchServer.msg = "Camera h moved LEFT to " + str(ScratchServer.Camera_H_Pos)
        print(ScratchServer.msg)
        return ScratchServer.msg

    
    def cameraRight(self, angle):
        try:
            angle = int(angle)
            ScratchServer.Camera_H_Pos =  90 - angle
            ScratchServer.Camera_H_Pos = constrain(ScratchServer.Camera_H_Pos, self.SERVO_MIN_ANGLE, self.SERVO_MAX_ANGLE)
            self.tcp.sendData(cmd.CMD_CAMERA_RIGHT + str(ScratchServer.Camera_H_Pos))
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        ScratchServer.msg = "Camera h moved RIGHT to " + str(ScratchServer.Camera_H_Pos)
        print(ScratchServer.msg)
        return ScratchServer.msg

    
    def lightRed(self):
        try:
            self.tcp.sendData(cmd.CMD_RGB_R)  
            ScratchServer.msg = "Light to Red"
            print(ScratchServer.msg)
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        return ScratchServer.msg

    
    def lightGreen(self):
        try:
            self.tcp.sendData(cmd.CMD_RGB_G)    
            ScratchServer.msg = "Light to Green"
            print(ScratchServer.msg)
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        return ScratchServer.msg

    
    def lightBlue(self):
        try:
            self.tcp.sendData(cmd.CMD_RGB_B)
            ScratchServer.msg = "Light to Blue"
            print(ScratchServer.msg)
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        return ScratchServer.msg

    
    def buzz(self, duration):
        try:
            duration = int(duration)
            print("Buzzing started")
            self.tcp.sendData(cmd.CMD_BUZZER_ALARM+"1")        
            time.sleep(float(duration) / 1000)
            self.tcp.sendData(cmd.CMD_BUZZER_ALARM+"0")        
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        ScratchServer.msg = "Buzzed for " + str(duration) + "ms"
        print(ScratchServer.msg)
        return ScratchServer.msg

    
    def moveForward(self, speed):
        try:
            speed = int(speed)
            print("Moving Forward")
            self.setMoveSpeed(cmd.CMD_FORWARD, speed)
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        ScratchServer.msg = "Moving forward at speed " + str(speed)
        print(ScratchServer.msg)
        return ScratchServer.msg
    def moveBackward(self, speed):
        try:
            speed = int(speed)
            print("Moving Backward")
            self.setMoveSpeed(cmd.CMD_BACKWARD, speed)
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        ScratchServer.msg = "Moving Backward at speed " + str(speed)
        print(ScratchServer.msg)
        return ScratchServer.msg

    
    def stop(self):
        try:
            print("Stopping")
            self.tcp.sendData(cmd.CMD_STOP)
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        ScratchServer.msg = "Stopped"
        print(ScratchServer.msg)
        return ScratchServer.msg

    
    def stepForward(self, speed, duration):
        try:
            speed = int(speed)
            duration = int(duration)

            print("Stepping Forward")
            self.setMoveSpeed(cmd.CMD_FORWARD, speed)
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        ScratchServer.msg = "Stepping forward at speed " + str(speed)
        print(ScratchServer.msg)
        time.sleep(float(duration) / 1000)
        self.tcp.sendData(cmd.CMD_STOP)
        ScratchServer.msg2 = "Stopped moving after " + str(duration) + "ms"

        return ScratchServer.msg + "\n" + ScratchServer.msg2

    
    def stepBackward(self, speed, duration):
        try:
            speed = int(speed)
            duration = int(duration)
            print("Stepping Backward")
            self.setMoveSpeed(cmd.CMD_BACKWARD, speed)
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        ScratchServer.msg = "Stepping Backward at speed " + str(speed)
        print(ScratchServer.msg)
        time.sleep(float(duration) / 1000)
        self.tcp.sendData(cmd.CMD_STOP)
        ScratchServer.msg2 = "Stopped moving after " + str(duration) + "ms"

        return ScratchServer.msg + "\n" + ScratchServer.msg2

    
    def turnLeft(self, angle):
        try:
            angle = int(angle)
            print("Turning Left")
            self.tcp.sendData(cmd.CMD_TURN_LEFT + str(angle))
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        ScratchServer.msg = "Turned Left to " + str(angle)
        print(ScratchServer.msg)
        return ScratchServer.msg

    
    def center(self):
        try:
            print("Centering")
            self.tcp.sendData(cmd.CMD_TURN_CENTER + str(90))
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        ScratchServer.msg = "Centered"
        print(ScratchServer.msg)
        return ScratchServer.msg

    
    def turnRight(self, angle):
        try:
            angle = int(angle)
            print("Turning Right")
            self.tcp.sendData(cmd.CMD_TURN_RIGHT + str(angle))
        except Exception as e:
            ScratchServer.lastError = "Error: " + e
            print(ScratchServer.lastError)
            return ScratchServer.lastError

        ScratchServer.msg = "Turned Right to " + str(angle)
        print(ScratchServer.msg)
        return ScratchServer.msg

            
    def setMoveSpeed(self, CMD, spd):
        self.tcp.sendData(CMD + str(float(spd)/3))
        time.sleep(0.07)
        self.tcp.sendData(CMD + str(float(spd)/3*2))
        time.sleep(0.07)
        self.tcp.sendData(CMD + str(spd))
     
            
ScratchServer.iSonic = 0
httpd = HTTPServer(('127.0.0.1', 8085), ScratchServer)

httpd.serve_forever()
    


