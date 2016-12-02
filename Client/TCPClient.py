# -*- coding: utf-8 -*-
"""
 ******************************************************************************
 * File  TCPClient.py
 * Author  Freenove (http://www.freenove.com)
 * Date    2016/11/14
 ******************************************************************************
 * Brief
 *   This is the Class TCPClient.
 ******************************************************************************
 * Copyright
 *   Copyright © Freenove (http://www.freenove.com)
 * License
 *   Creative Commons Attribution ShareAlike 3.0 
 *   (http://creativecommons.org/licenses/by-sa/3.0/legalcode)
 ******************************************************************************
"""


from socket import *

class TCPClient:
    #HOST = '127.0.0.1'
    HOST = '192.168.1.108'
    PORT = 12345
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    
    def __init__(self):
        #self.client = socket(AF_INET, SOCK_STREAM)
        pass
        
    def connectToServer(self, address = ADDR):
        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.settimeout(5)
        self.client.connect(address)
    
    def disConnect(self):        
        try:
            self.client.close()
        except Exception, e:
            print Exception, "Disconnect error:", e
        
    def sendData(self, data):
        try:
            self.client.send(data)
        except Exception, e:
            print Exception, "Send TCP Data error:", e
    
    def recvData(self):
        try:
            return self.client.recv(self.BUFSIZ)
        except Exception, e:
            print Exception, "Recv TCP Data error:", e
        
        
