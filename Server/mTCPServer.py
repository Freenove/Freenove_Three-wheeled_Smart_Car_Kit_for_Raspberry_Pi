#-*- coding: utf-8 -*-
"""
 ******************************************************************************
 * File  mTCPServer.py
 * Author  Freenove (http://www.freenove.com)
 * Date    2016/11/14
 ******************************************************************************
 * Brief
 *   This is the Class mTCPServer.
 ******************************************************************************
 * Copyright
 *   Copyright © Freenove (http://www.freenove.com)
 * License
 *   Creative Commons Attribution ShareAlike 3.0 
 *   (http://creativecommons.org/licenses/by-sa/3.0/legalcode)
 ******************************************************************************
"""
from socket import *
import threading
from Command import COMMAND as cmd
from mDev import *
mdev = mDEV()
class mTCPServer(threading.Thread):
    HOST = ''
    PORT = 12345
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    
    def __init__(self):
        #self.client = socket(AF_INET, SOCK_STREAM)
        super(mTCPServer,self).__init__()
        self.setName("Name TCP Server")
        pass
        
    def run(self):
		self.startTCPServer()
		self.tcpLink()
		
    def startTCPServer(self):
        self.sock = socket(AF_INET, SOCK_STREAM)
        try:
			self.sock.bind(self.ADDR)
        except Exception,e:
			print "Bind Error : ",e
			self.tcpClientSock, self.addr = self.sock.accept()
			self.sock.bind(self.ADDR)
        self.sock.listen(1)        
        #self.t = threading.Thread(target = self.tcpLink)
        #self.t.setName("TCP Server Thread...")
        #self.t.start()
        
        #self.t.setDaemon(True)
        print "TCP Server Thread Starting ... "

    def tcpLink(self):
        while True:
            print "Wating for connect ... "
            try:
			    self.tcpClientSock, self.addr = self.sock.accept()
			    print "Connect from ", self.addr
            except Exception ,  e:
				print "sock closed! Error: ",e
				try:
					self.tcpClientSock.close()
				except Exception ,  e:
					print "Client close Error",e
				self.sock.shutdown(2)
				self.sock.close()             
				break			
            
            while True:
                try:
                    RecvData_ALL = self.tcpClientSock.recv(self.BUFSIZ)
                except Exception ,  e:
                    print e
                    self.tcpClientSock.close()
                    break
                if not RecvData_ALL:
                    break
                #print RecvData_ALL
                RecvData_Array = RecvData_ALL.split(">")
                print RecvData_Array
                for RecvData in RecvData_Array:                    
                    if RecvData == "":
                        continue
                    print "RecvData  : ", RecvData
                    if cmd.CMD_FORWARD[1:]  in RecvData:
                        try:
                            value = int(filter(str.isdigit, RecvData))
                        except Exception,e:
                            print e
                            continue
                        mdev.writeReg(mdev.CMD_DIR1,1)
                        mdev.writeReg(mdev.CMD_DIR2,1)
                        mdev.writeReg(mdev.CMD_PWM1,value*10)
                        mdev.writeReg(mdev.CMD_PWM2,value*10)
                    elif cmd.CMD_BACKWARD[1:]   in RecvData:
                        value = int(filter(str.isdigit, RecvData))
                        mdev.writeReg(mdev.CMD_DIR1,0)
                        mdev.writeReg(mdev.CMD_DIR2,0)
                        mdev.writeReg(mdev.CMD_PWM1,value*10)
                        mdev.writeReg(mdev.CMD_PWM2,value*10)
                        pass
                    elif cmd.CMD_TURN_LEFT[1:]   in RecvData:
                        value = int(filter(str.isdigit, RecvData))
                        mdev.writeReg(mdev.CMD_SERVO1,numMap(90+value,0,180,500,2500))
                        pass
                    elif cmd.CMD_TURN_RIGHT[1:]   in RecvData:
                        value = int(filter(str.isdigit, RecvData))
                        mdev.writeReg(mdev.CMD_SERVO1,numMap(90-value,0,180,500,2500))
                        pass
                    elif cmd.CMD_STOP[1:]   in RecvData:
                        mdev.writeReg(mdev.CMD_PWM1,0)
                        mdev.writeReg(mdev.CMD_PWM2,0)
                        pass
                    elif cmd.CMD_TURN_CENTER[1:]   in RecvData:
                        value = int(filter(str.isdigit, RecvData))
                        mdev.writeReg(mdev.CMD_SERVO1,numMap(value,0,180,500,2500))
                        pass
                    elif cmd.CMD_CAMERA_UP[1:]   in RecvData:
                        value = int(filter(str.isdigit, RecvData))
                        mdev.writeReg(mdev.CMD_SERVO3,numMap(value,0,180,500,2500))
                        pass
                    elif cmd.CMD_CAMERA_DOWN[1:]   in RecvData:
                        value = int(filter(str.isdigit, RecvData))
                        mdev.writeReg(mdev.CMD_SERVO3,numMap(value,0,180,500,2500))
                        pass
                    elif cmd.CMD_CAMERA_LEFT[1:]   in RecvData:
                        value = int(filter(str.isdigit, RecvData))
                        mdev.writeReg(mdev.CMD_SERVO2,numMap(value,0,180,500,2500))
                        pass
                    elif cmd.CMD_CAMERA_RIGHT[1:]   in RecvData:
                        value = int(filter(str.isdigit, RecvData))
                        mdev.writeReg(mdev.CMD_SERVO2,numMap(value,0,180,500,2500))
                        pass
                    elif cmd.CMD_CAMERA_STOP[1:]   in RecvData:
                        pass
                    elif cmd.CMD_CAMERA_CENTER[1:]   in RecvData:
                        pass
                    elif cmd.CMD_SPEED_SLIDER[1:]  in RecvData:
                        value = int(filter(str.isdigit, RecvData))
                        print value
                        pass
                    elif cmd.CMD_DIR_SLIDER[1:]   in RecvData :
                        value = int(filter(str.isdigit, RecvData))
                        print value
                        pass
                    elif cmd.CMD_CAMERA_SLIDER[1:]   in RecvData :
                        value = int(filter(str.isdigit, RecvData))
                        print value  
                    elif cmd.CMD_BUZZER_ALARM[1:]  in RecvData:
						try:
							value = int(filter(str.isdigit, RecvData))
							if value != 0:
								mdev.writeReg(mdev.CMD_BUZZER,2000)
							elif value == 0:               		
								mdev.writeReg(mdev.CMD_BUZZER,0)
						except Exception ,  e:
							print "Command without parameters"
							if mdev.Is_Buzzer_State_True is True:
								mdev.Is_Buzzer_State_True = False
								mdev.writeReg(mdev.CMD_BUZZER,0)
							elif mdev.Is_Buzzer_State_True is False:                		
								mdev.Is_Buzzer_State_True = True
								mdev.writeReg(mdev.CMD_BUZZER,2000)
						
                    elif cmd.CMD_RGB_B[1:]  in RecvData:
                        if mdev.Is_IO3_State_True is True:
                            mdev.Is_IO3_State_True = False
                            mdev.writeReg(mdev.CMD_IO3,0)
                        elif mdev.Is_IO3_State_True is False:
                            mdev.Is_IO3_State_True = True
                            mdev.writeReg(mdev.CMD_IO3,1)
                    elif cmd.CMD_RGB_R[1:]  in RecvData:
                        if mdev.Is_IO1_State_True is True:
                            mdev.Is_IO1_State_True = False
                            mdev.writeReg(mdev.CMD_IO1,0)
                        elif mdev.Is_IO1_State_True is False:
                            mdev.Is_IO1_State_True = True
                            mdev.writeReg(mdev.CMD_IO1,1)
                    elif cmd.CMD_RGB_G[1:]  in RecvData:
                        if mdev.Is_IO2_State_True is True:
                            mdev.Is_IO2_State_True = False
                            mdev.writeReg(mdev.CMD_IO2,0)
                        elif mdev.Is_IO2_State_True is False:
                            mdev.Is_IO2_State_True = True
                            mdev.writeReg(mdev.CMD_IO2,1)    
                    elif cmd.CMD_ULTRASONIC[1:]  in RecvData:						
						sonic = mdev.getSonic()
						self.sendData(str(sonic))
            #time.sleep(1)
    def stopTCPServer(self):
        pass
        try:
			self.tcpClientSock.close()
        except Exception ,  e:
			print "Client close Error",e
        self.sock.shutdown(2)
        self.sock.close()
        
    def sendData(self, data):
        self.tcpClientSock.send(data)
        
if __name__ == "__main__":
    import sys
    tcp = TCPServer()
    tcp.startTCPServer()
    sys.exit(exec_())
